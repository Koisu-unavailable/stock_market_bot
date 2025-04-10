import discord
from database.firebase.User import User
from database.firebase.databse_user import get_user_by_id, add_or_update_user

async def get_user_from_interaction(
    interaction: discord.Interaction
) -> User:
    """Gets the user from the reaction, if they don't exist, create them and give them the starting amount of money."""
    userId = interaction.user.id
    user = get_user_by_id(userId)

    if user is None:
        user = User(userId, {}, 10**5)  # $10000 to start
        add_or_update_user(user)
    return user