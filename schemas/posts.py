import sys

from pydantic import BaseModel, field_validator, ValidationError


MAX_SIZE = 1024 * 1024


class PostsRegister(BaseModel):
    post: str

    @field_validator("post")
    @classmethod
    def size_of_text(cls, v: str) -> str:
        # Subtracting size to offset the extra bytes taken as python object
        if sys.getsizeof(v) - sys.getsizeof('') > MAX_SIZE:
            raise ValidationError("post value exceeds 1MB")
        return v


class PostsBase(BaseModel):
    postID: int


class PostDelete(PostsBase):
    pass


class PostRegisterResponse(PostsBase):
    pass


class PostGet(PostsBase):
    postID: int
    post: str
