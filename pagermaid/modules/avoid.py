""" PagerMaid module for different ways to avoid users. """from pyrogram import Client, filters, ContinuePropagationfrom pagermaid import sqlite, logfrom pagermaid.utils import lang, alias_command, Message, edit_or_replyfrom pagermaid.listener import listener, raw_listener@listener(is_plugin=False, outgoing=True, command=alias_command('ghost'),          description=lang('ghost_des'),          parameters="<true|false|status>")async def ghost(client: Client, message: Message):    """ Toggles ghosting of a user. """    if len(message.parameter) != 1:        await edit_or_reply(message, f"{lang('error_prefix')}{lang('arg_error')}")        return    myself = await client.get_me()    self_user_id = myself.id    if message.parameter[0] == "true":        if message.chat.id == self_user_id:            return await edit_or_reply(message, lang('ghost_e_mark'))        sqlite["ghosted.chat_id." + str(message.chat_id)] = True        await message.delete()        await log(f"{lang('ghost_set_f')} ChatID {str(message.chat_id)} {lang('ghost_set_l')}")    elif message.parameter[0] == "false":        if message.chat_id == self_user_id:            await edit_or_reply(message, lang('ghost_e_mark'))            return        try:            del sqlite["ghosted.chat_id." + str(message.chat_id)]        except KeyError:            return await edit_or_reply(message, lang('ghost_e_noexist'))        await message.delete()        await log(f"{lang('ghost_set_f')} ChatID {str(message.chat_id)} {lang('ghost_cancel')}")    elif message.parameter[0] == "status":        if sqlite.get("ghosted.chat_id." + str(message.chat_id), None):            await edit_or_reply(message, lang('ghost_e_exist'))        else:            await edit_or_reply(message, lang('ghost_e_noexist'))    else:        await edit_or_reply(message, f"{lang('error_prefix')}{lang('arg_error')}")@listener(is_plugin=False, outgoing=True, command=alias_command('deny'),          description=lang('deny_des'),          parameters="<true|false|status>")async def deny(client: Client, message: Message):    """ Toggles denying of a user. """    if len(message.parameter) != 1:        await edit_or_reply(message, f"{lang('error_prefix')}{lang('arg_error')}")        return    myself = await client.get_me()    self_user_id = myself.id    if message.parameter[0] == "true":        if message.chat.id == self_user_id:            return await edit_or_reply(message, lang('ghost_e_mark'))        sqlite["denied.chat_id." + str(message.chat_id)] = True        await message.delete()        await log(f"ChatID {str(message.chat_id)} {lang('deny_set')}")    elif message.parameter[0] == "false":        if message.chat_id == self_user_id:            await edit_or_reply(message, lang('ghost_e_mark'))            return        try:            del sqlite["denied.chat_id." + str(message.chat_id)]        except KeyError:            return await edit_or_reply(message, lang('deny_e_noexist'))        await message.delete()        await log(f"ChatID {str(message.chat_id)} {lang('deny_cancel')}")    elif message.parameter[0] == "status":        if sqlite.get("denied.chat_id." + str(message.chat_id), None):            await edit_or_reply(message, lang('deny_e_exist'))        else:            await edit_or_reply(message, lang('deny_e_noexist'))    else:        await edit_or_reply(message, f"{lang('error_prefix')}{lang('arg_error')}")@raw_listener(filters.incoming & ~filters.edited)async def set_read_acknowledgement(client: Client, message: Message):    """ Event handler to infinitely read ghosted messages. """    if sqlite.get("ghosted.chat_id." + str(message.chat.id), None):        await client.read_history(message.chat.id)    raise ContinuePropagation@raw_listener(filters.incoming & ~filters.edited)async def message_removal(client: Client, message: Message):    """ Event handler to infinitely delete denied messages. """    if sqlite.get("denied.chat_id." + str(message.chat.id), None):        try:            await message.delete()        except Exception as e:  # noqa            pass    raise ContinuePropagation