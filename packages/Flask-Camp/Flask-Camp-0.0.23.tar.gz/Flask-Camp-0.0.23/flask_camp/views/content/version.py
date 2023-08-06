from flask import request
from werkzeug.exceptions import NotFound, BadRequest

from flask_camp._schemas import schema
from flask_camp._services._security import allow
from flask_camp._utils import cook, current_api, JsonResponse
from flask_camp.models._document import DocumentVersion, Document

rule = "/document/version<int:version_id>"


@allow("anonymous", "authenticated", allow_blocked=True)
def get(version_id):
    """Get a given version of a document"""

    version = DocumentVersion.get(id=version_id)

    if version is None:
        raise NotFound()

    return JsonResponse({"status": "ok", "document": cook(version.as_dict())})


@allow("moderator")
@schema("modify_version.json")
def put(version_id):
    """Modify a version of a document. The only possible modification is hide/unhide a version"""
    version = DocumentVersion.get(id=version_id, with_for_update=True)

    if version is None:
        raise NotFound()

    old_last_version = version.document.last_version
    hidden = request.get_json()["version"]["hidden"]
    version.hidden = hidden
    current_api.database.session.flush()

    document = Document.get(id=version.document_id, with_for_update=True)
    document.update_last_version_id()

    needs_update = old_last_version.id != version.document.last_version_id

    if needs_update:
        current_api.on_document_save(document=document, old_version=old_last_version, new_version=document.last_version)

    current_api.add_log("hide_version" if hidden else "unhide_version", version=version, document=version.document)
    current_api.database.session.commit()

    if needs_update:
        version.document.clear_memory_cache()

    return JsonResponse({"status": "ok"})


@allow("admin")
@schema("action_with_comment.json")
def delete(version_id):
    """Delete a version of a document (only for admins)"""
    version = DocumentVersion.get(id=version_id, with_for_update=True)

    if version is None:
        raise NotFound()

    if DocumentVersion.query.filter_by(document_id=version.document_id).count() <= 1:
        raise BadRequest("Can't delete last version of a document")

    old_last_version = version.document.last_version
    document = Document.get(id=version.document_id, with_for_update=True)

    document.update_last_version_id(forbidden_id=version.id)
    needs_update = old_last_version.id != version.document.last_version_id

    if needs_update:
        current_api.on_document_save(document=document, old_version=old_last_version, new_version=document.last_version)

    current_api.database.session.delete(version)
    current_api.add_log("delete_version", version=version, document=version.document)
    current_api.database.session.commit()

    if needs_update:
        version.document.clear_memory_cache()

    return JsonResponse({"status": "ok"})
