from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from async_lru import alru_cache

from deps import get_current_user, DBSession, CURR_USER
from models.models import Posts
from schemas.posts import PostsRegister, PostRegisterResponse


router = APIRouter(
    prefix="/post",
    dependencies=[Depends(get_current_user)]
)


@alru_cache(ttl=5 * 60)
async def crud_get_post(session: DBSession, user_email: str):
    query = select(Posts).where(Posts.user_email == user_email)
    result = (await session.scalars(query)).all()

    return result


@router.post(
    "/add_post",
    response_model=PostRegisterResponse
)
async def add_post(
    new_post: PostsRegister,
    session: DBSession,
    curr_user: CURR_USER
):
    new_post_row = Posts(
        post=new_post.post,
        user_email=curr_user
    )

    session.add(new_post_row)
    await session.commit()
    await session.refresh(new_post_row)

    return PostRegisterResponse(
        postID=new_post_row.postID
    )


@router.get(
    "/get_posts",
)
async def get_post(session: DBSession, curr_user: CURR_USER):

    return (await crud_get_post(session, curr_user))


@router.delete(
    "/delete_post/{post_id}"
)
async def delete_post(post_id: int, session: DBSession, curr_user: CURR_USER):
    ddl = delete(Posts).where(Posts.user_email ==
                              curr_user, Posts.postID == post_id)
    await session.execute(ddl)
    await session.commit()

    crud_get_post.cache_invalidate(session=session, user_email=curr_user)

    return f"{post_id} deleted!"
