from aiogram import F, Router
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, JOIN_TRANSITION
    
    
    
router = Router()

# @router.my_chat_member(
#     ChatMemberUpdatedFilter(
#         member_status_changed=
#         IS_NOT_MEMBER >> IS_MEMBER
#     )
# )
@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=JOIN_TRANSITION
    )
)
def paass():
    pass