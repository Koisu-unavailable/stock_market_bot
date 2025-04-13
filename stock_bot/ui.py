"""
All ui's for discord bot
"""

from __future__ import annotations

from typing import List

import discord

import cache
from stock_bot.transaction import BuyBroker, TransactionResult
from utils import database


def broker_shop_embed_factory(broker_id: str):
    shop = discord.Embed(title="Buy a Broker")
    try:
        broker_name = cache.BROKERS[broker_id]["name"]
        broker_image_url = cache.BROKERS[broker_id]["image_url"]
        broker_price = cache.BROKERS[broker_id]["price"]
        broker_rarity = cache.BROKERS[broker_id]["rarity"]
    except KeyError:
        raise ValueError("Invalid Broker ID")
    shop.add_field(name="Broker Name", value=broker_name).add_field(
        name="Price", value=broker_price
    ).set_image(url=broker_image_url).add_field(
        name="Rarity", value=cache.BROKER_RARITIES[broker_rarity]
    )
    return shop


class ChangeBrokerInBrokerShop(discord.ui.Button):
    def __init__(
        self,
        *,
        style=discord.ButtonStyle.secondary,
        label=None,
        disabled=False,
        custom_id=None,
        url=None,
        emoji=None,
        row=None,
        sku_id=None,
        back: bool,
        embeds: List[discord.Embed],
        shop_interaction: discord.Interaction,
    ):
        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row,
            sku_id=sku_id,
        )
        # if not isinstance(self.view, Shop_View):  <-- doesn't work
        #     raise ValueError("This must be instatiated with the Shop_View class")
        self.back = back
        self.embeds = embeds
        self.shop_interaction = shop_interaction

        if self.back:
            self.disabled = True

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not self.back:
            self.view.current_broker += 1
        else:
            self.view.current_broker -= 1
        self.disable_me_if_I_should_be()
        await interaction.edit_original_response(
            embed=self.embeds[self.view.current_broker], view=self.view
        )

    # doodoo code
    def disable_me_if_I_should_be(self):
        if self.view.current_broker == 0:
            for item in self.view.children:
                try:
                    if item.back:
                        item.disabled = True

                        break
                except AttributeError:
                    continue  # item is not button
        elif self.view.current_broker >= len(self.embeds) - 1:
            for item in self.view.children:
                try:
                    if not item.back:
                        item.disabled = True

                        break
                except AttributeError:
                    continue  # item is not button
        if 0 < self.view.current_broker:
            for item in self.view.children:
                try:
                    if item.back:
                        item.disabled = False

                except AttributeError:
                    continue  # item is not button
        if self.view.current_broker < len(self.embeds) - 1:
            for item in self.view.children:
                try:
                    if not item.back:
                        item.disabled = False

                except AttributeError:
                    continue  # item is not button

    @property
    def view(self) -> Shop_View:  # proper type
        return super().view


class Shop_View(discord.ui.View):
    def __init__(self, *, timeout=180, owner: discord.User, brokers: List[str]):
        super().__init__(timeout=timeout)
        self.current_broker = 0
        self.owner = owner
        self.brokers = brokers

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Buy Buy Buy!")
    async def buy(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer()
        broker_id = self.brokers[self.current_broker]
        broker = cache.BROKERS[broker_id]
        price = broker["price"]
        transaction = BuyBroker(
            price, await database.get_user_from_interaction(interaction), [], broker_id
        )
        result = transaction.complete()
        match result:
            case TransactionResult.Poor:
                await interaction.followup.send(
                    "Your to poor for this broker", ephemeral=True
                )
            case TransactionResult.Success:
                await interaction.followup.send(
                    "You now have this broker!", ephemeral=True
                )

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.owner:
            if interaction.response.is_done:
                await interaction.followup.send("This is not your shop.")
            else:
                await interaction.response.send_message("This is not your shop.")
            return False
        return True
