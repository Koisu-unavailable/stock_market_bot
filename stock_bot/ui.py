"""
All ui's for discord bot
"""

from typing import List
import discord

import cache
from recordclass import RecordClass

def broker_shop_factory(broker_id: str):
    shop = discord.Embed(title="Buy a Broker")
    try:
        broker_name = cache.BROKERS[broker_id]["name"]
        broker_image_url = cache.BROKERS[broker_id]["image_url"]
    except KeyError:
        raise ValueError("Invalid Broker ID")
    shop.add_field(name="Broker Name", value=broker_name)
    shop.set_image(url=broker_image_url)
    return shop


class Shop_State(RecordClass):
    current_broker: int

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
        owner: discord.User,
        back: bool,
        embeds: List[discord.Embed],
        shop_interaction: discord.Interaction,
        shop_state: Shop_State
    ):
        self.owner = owner
        self.back = back
        self.embeds = embeds
        self.shop_interaction = shop_interaction
        self.state = shop_state
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
        if self.back:
            self.disabled = True
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user != self.owner:
            await interaction.followup.send("You may not touch this button.")
            return
        
        if self.back:
            self.state.current_broker -= 1
            if self.state.current_broker == 0:
                self.disabled = True
            else:
                self.disabled = False
            await interaction.edit_original_response(embed=self.embeds[self.state.current_broker])
            return
        self.state.current_broker += 1
        if self.state.current_broker >= len(self.embeds) -1:
            
            self.disabled = True
        else:
            
            self.disabled = False
        await interaction.edit_original_response(embed=self.embeds[self.state.current_broker])    
        
        
        

    
