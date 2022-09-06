from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext
from pydantic.validators import List

from domains.galleries.services.gallery_services import GalleriesService
from domains.organizations.services.organization_services import OrganizationsService
from domains.users.services.user_services import UserService
from models.gallery import Gallery
from models.response import Response

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/", response_model=Gallery, response_description="Successfully registered gallery.")
async def add_gallery(new_gallery: Gallery = Body(...)):
    """Registers a new gallery within the space.
    """
    gallery_exists = await Gallery.find_one(Gallery.name == new_gallery.name)
    if gallery_exists:
        raise HTTPException(
            status_code=409,
            detail="A gallery already exists by that name."
        )
    user_service = UserService()
    for i in range(0, len(new_gallery.userPids)):
        await user_service.validate_exists(pid=new_gallery.userPids[i])

    organization_service = OrganizationsService()
    await organization_service.validate_exists(pid=new_gallery.organizationPid)

    gallery_services = GalleriesService()
    await gallery_services.add_document(new_gallery)
    return new_gallery


@router.get("/", response_description="Galleries retrieved", response_model=Response[Gallery])
async def get_galleries(q: str | None = None, limit: int | None = None, offset: int | None = None, sort: str | None = None):
    """Gets all galleries using the user defined parameters.
    """
    gallery_service = GalleriesService()
    galleries = await gallery_service.get_all(q=q, limit=limit, offset=offset, sort=sort)
    return Response(status_code=200,
                    response_type='success',
                    description="Galleries retrieved successfully.",
                    data=galleries)


@router.get("/{pid}", response_description="Gallery data retrieved", response_model=Response[Gallery])
async def get_gallery(pid: str):
    """Retrieves a gallery by ID.
    """
    gallery_service = GalleriesService()
    gallery = await gallery_service.validate_exists(pid=pid)
    return Response(status_code=200, response_type='success', description='Gallery retrieved.', data=[gallery])


@router.patch("/{pid}", response_model=Response, response_description="Successfully patched gallery.")
async def patch_gallery(pid: str, patch_list: List[object] = Body(...)):
    """Patches a gallery within the space.
    """
    gallery_service = GalleriesService()
    await gallery_service.patch(pid=pid, patch_document_list=patch_list)
    return Response(status_code=204, response_type='success', description="Gallery patched successfully.")


@router.delete("/{pid}", response_description="Gallery successfully deleted.", response_model=Response)
async def delete_gallery(pid: str):
    """Deletes a gallery.
    """
    gallery_service = GalleriesService()
    await gallery_service.delete_document(pid=pid)
    return Response(status_code=200, response_type="success", description="Gallery deleted.")
