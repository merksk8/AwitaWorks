# INICIO DE CLIENTE DE DISCORD
print("== INICIANDO AWITAWORKS by merk_cat ==")

# IMPORTACIONES
print(">>Importando Discord")
import discord
from discord.ext import commands
from dpyConsole import Console

# CUSTOM IMPORTS
print(">>Importando archivos custom")
print(">>Importando config")
import config as config
print(">>Importando db")
import modules.db as db
print(">>Importando botchannels")
import modules.botchannels as botchannels
print(">>Importando botutils")
import modules.botutils as botutils
print(">>Importando botworks")
import modules.botworks as botworks

bot = commands.Bot(command_prefix=config.commandPrefix)

############################################################################################
# ON READY
@bot.event
async def on_ready():
    print('im in as {}'.format(bot.user))
    print('Server ON')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=config.statusText))

@bot.event
async def on_error(event):
    print(event)
    
@bot.event
async def on_guild_join(guild):
    print("Me he unido al servidor: " + guild.name + " con id " + str(guild.id) )

# ON MESSAGE
@bot.event
async def on_message(message):

    if not message.guild and message.author != bot.user:
        await message.author.send(
            "¡Hola " + message.author.name + ", soy un bot :robot: ! \n" + 
            "> :no_entry: No puedo leer mensajes privados. \n" + 
            "> :white_check_mark: Los comandos **siempre** se utilizan en las salas que me tengan activado. \n" + 
            "> :question: Utiliza **!ayuda** en cualquier sala donde tenga permisos para poder ayudarte. \n" + 
            "> :bug: En caso de bug, contacta con merk_cat#2475, mi creador :alien: "
        )
        
    else:
        if db.mydb.is_connected() == False:
            db.mydb.reconnect()
        
        await bot.process_commands(message)

        
# Gestionar las reacciones
@bot.event
async def on_raw_reaction_add(reactionEvent):
    
    emoteName = reactionEvent.emoji.name
    member_id = reactionEvent.user_id
    channel = bot.get_channel(reactionEvent.channel_id)
    msg = await channel.fetch_message(reactionEvent.message_id)
    
    # Comprobar que esté activo en el canal y que no sea una reacción del bot
    if botchannels.checkRoomToConfig(msg) == False or reactionEvent.member.id == bot.user.id:
        return
    
    # Comprobar que sea válido - Que el bot haya reaccionado al mensaje
    checkValidMessage = False
    for react in msg.reactions:
        async for user in react.users():
            if user.id == bot.user.id:
                checkValidMessage = True
    
    if checkValidMessage == False:
        # await msg.channel.send("Sólo sirve donde haya reaccionado :( ")
        return
    
    # Comprobar que el usuario que reacciona sea el mismo que el del mensaje
    if reactionEvent.member.id != msg.author.id and not reactionEvent.member.permissions_in(channel).administrator:
        await msg.channel.send('<@' + str(reactionEvent.member.id) + '> ' + " :no_entry_sign: Sólo puedes eliminar tus propios registros.")
        return
    
    # Comprobar el marcar con X - Eliminar registro
    if emoteName == "❌":
        
        if botworks.checkIfRegisterExists(msg) == False:
            await msg.channel.send('<@' + str(reactionEvent.member.id) + '> ' + " :no_entry_sign: El registro ya estaba eliminado")
            return
        
        botworks.deleteRegisterByMessage(msg)
        await msg.reply('<@' + str(reactionEvent.member.id) + '> ' + " :white_check_mark:  Se ha eliminado el registro correspondiente")
        
    # Comprobar para restaurar registro
    elif emoteName == "✅":
        if botworks.checkIfDeletedRegisterExists(msg) == False:
            await msg.channel.send('<@' + str(reactionEvent.member.id) + '> ' + " :no_entry_sign: El registro no estaba eliminado")
            return
        
        botworks.restoreRegisterByMessage(msg)
        await msg.reply('<@' + str(reactionEvent.member.id) + '> ' + " :white_check_mark: Se ha restaurado el registro.")
            
@bot.event
async def on_command_error(ctx, error ):

    if db.mydb.is_connected() == False:
        db.mydb.reconnect()

    if isinstance(error, commands.BadArgument ):
        await botutils.SendMessage( ctx, " :no_entry_sign: Error de parámetro. Si es un usuario, mencionalo con '@' , si es un decimal utiliza el punto '.' ")
        return

    if isinstance(error, commands.CommandNotFound ):
        await botutils.SendMessage( ctx, " :no_entry_sign: El comando no existe")
        return

    if isinstance(error, commands.MissingRequiredArgument ):
        await botutils.SendMessage( ctx, " :no_entry_sign: Faltan uno o más parámetros para usar el comando")
        return
    
    if isinstance(error, commands.CheckFailure) :
        return

    await botutils.SendMessage( ctx, " :bug: Error no reconocido: " + str(error) )

# FUNCION PARA COMPROBAR PERMISOS DE ADMIN
async def onlyAdministrator(ctx):
    if ctx.message.author.permissions_in(ctx.channel).administrator:
        return True
    else:
        await botutils.SendMessage( ctx, ' :no_entry_sign: No tienes permiso para usar el comando')
        return False


#COMANDO ID
@bot.command(pass_context=True, name = "id" )
async def _myid(ctx):
    await botutils.SendMessage( ctx, "Tu id es: " + str(ctx.author.id))

#COMANDO LIMPIAR
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    await ctx.send('Limpiado por {}'.format(ctx.author.mention))

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await botutils.SendMessage( ctx, ' :no_entry_sign: No tienes permiso para usar el comando')

############################################################################################
# REGISTRAR COMANDOS
@bot.command( name = config.commandTotal )
async def _totalSimple(ctx: commands.Context, target: discord.Member = None):

    if botchannels.checkRoomToConfig(ctx) == False:
        return

    if target is None:

        targetId = ctx.author.id
        totalMinutes = botworks.checkTotalUserTime(targetId, ctx)

        if totalMinutes == 0:
            await botutils.SendMessage( ctx, ' :no_entry_sign: No hay registros de ninguna jornada terminada. Si sólo tienes una jornada y no está terminada, utiliza !comprobar' )
        else:
            hours = totalMinutes//60
            minutes = totalMinutes - (hours*60)

            await ctx.author.send('> <@' + str(targetId) + '> :white_check_mark: Llevas un total de ' + str(hours).zfill(2) + ':' + str(minutes).zfill(2) + 'h trabajadas.' )
            await ctx.message.delete() 
       
    else:

        if ctx.message.author.permissions_in(ctx.channel).administrator:

            targetId = target.id
            totalMinutes = botworks.checkTotalUserTime(targetId, ctx)

            if totalMinutes == 0:
                await botutils.SendMessageById( ctx, targetId, 'No hay registros de ninguna jornada terminada.' )
            else:
                hours = totalMinutes//60
                minutes = totalMinutes - (hours*60)

                await ctx.author.send( 
                    '> <@' + str(targetId) + '> :white_check_mark: Lleva un total de **' + str(hours).zfill(2) + ':' + str(minutes).zfill(2) + 'h** trabajadas.'
                )

                await ctx.message.delete()


        else:
            await botutils.SendMessage( ctx, ' :no_entry_sign: No tienes permiso para usar el comando con otro usuario.' )

# COMANDO TOTAL
@bot.command( name = config.commandPagar )
async def _pagar(ctx: commands.Context, target: discord.Member, price: float):

    if botchannels.checkRoomToConfig(ctx) == False:
        return

    # Si tiene mencion es que se busca otro usuario
    if target is None:
        targetId = ctx.author.id
        totalMinutes = botworks.checkTotalUserTime(targetId, ctx)

        if totalMinutes == 0:
            await botutils.SendMessage( ctx, ' :no_entry_sign: No hay registros de ninguna jornada terminada. Si sólo tienes una jornada y no está terminada, utiliza !comprobar' )
        else:
            hours = totalMinutes//60
            minutes = totalMinutes - (hours*60)
            await botutils.SendMessage( ctx, ' :white_check_mark: Llevas un total de ' + str(hours).zfill(2) + ':' + str(minutes).zfill(2) + 'h trabajadas.' )
       
    else:

        if ctx.message.author.permissions_in(ctx.channel).administrator:

            targetId = target.id
            totalMinutes = botworks.checkTotalUserTime(targetId, ctx)

            if totalMinutes == 0:
                await botutils.SendMessageById( ctx, targetId, ' :no_entry_sign: No hay registros de ninguna jornada terminada. Si sólo tienes una jornada y no está terminada, utiliza !comprobar' )
            else:
                hours = totalMinutes//60
                minutes = totalMinutes - (hours*60)
                # price = botchannels.getRoomPrice(ctx)
                totalHours = round( float(hours) + ( float(minutes) / 60.0 ) , 2 )
                totalPrice = round( float(totalHours) * float(price), 2 )

                await ctx.author.send( 
                    '📑 <@' + str(targetId) + '> Lleva un total de **' + str(hours).zfill(2) + ':' + str(minutes).zfill(2) + 'h** trabajadas. Resumen de jornadas: \n' + 
                    '----------------------------------------------------------------------\n' + 
                    botworks.checkTotalUserTimeExtended(targetId, ctx) +
                    '----------------------------------------------------------------------\n' + 
                    '🧾Resumen: ' +   str(totalHours) + 'h  X  ' +  str(price) + ' $/h \n' + 
                    '💰TOTAL: **' +  str(totalPrice) + " $. ** \n" + 
                    '*Recuerda utilizar el comando **!' + config.commandReset + ' <@' + str(targetId) + '>** en la sala de fichaje para reiniciar las horas al trabajador a cero.*'
                )

                await ctx.message.delete()


        else:
            await botutils.SendMessage( ctx, ' :no_entry_sign: No tienes permiso para usar el comando con otro usuario.' )

# COMANDO REINICIAR
@bot.command( name = config.commandReset )
async def _reset(ctx: commands.Context, target: discord.Member = None):
    if target is None:
        await botworks.deleteAllRegistersFromUser(ctx.author.id,  ctx)
    else:
        if ctx.message.author.permissions_in(ctx.channel).administrator:
            await botworks.deleteAllRegistersFromUser(target.id, ctx)
        else:
            await botutils.SendMessage( ctx, ' :no_entry_sign: No tienes permiso para usar el comando con otro usuario.' )

# COMANDO COMPROBAR
@bot.command( name = config.commandCheck )
async def _check(ctx: commands.Context):

    if botchannels.checkRoomToConfig(ctx) == False:
        return

    if botworks.checkIfAlreadyRegistered(ctx.author.id, ctx):
        totalMinutes = botworks.checkSessionUserTime(ctx.author.id, ctx)

        hours = totalMinutes//60
        minutes = totalMinutes - (hours*60)
        await botutils.SendMessage( ctx, ' :white_check_mark: Llevas un total de ' + str(hours).zfill(2) + ':' + str(minutes).zfill(2) + 'h trabajadas.' )
    else:
        await botutils.SendMessage( ctx, ' :no_entry_sign: No estás de servicio actualmente.' )


# COMANDO ENTRADA
@bot.command( name = config.commandEnter )
async def _enter(ctx: commands.Context):

    if botchannels.checkRoomToConfig(ctx) == False:
        return

    if botworks.checkIfAlreadyRegistered(ctx.author.id, ctx):
        await botutils.SendMessage( ctx, ' :no_entry_sign: Ya estás registrad@. Utiliza ' + config.commandCheck + ' para comprobar cuanto llevas en servicio.' )
    else:
        
        activeWorkers = botworks.getActiveWorkers(ctx)
        maxWorkers = botchannels.getMaxWorkers(ctx)
        
        if activeWorkers < maxWorkers or maxWorkers < 0:
            botworks.registerWorkUser(ctx.author.id, ctx)
            await botutils.SendMessage( ctx, ' :white_check_mark: Registrada la entrada. ¡A trabajar!' )
        else:
            await botutils.SendMessage( ctx, ' :no_entry_sign: Se ha llegado al máximo de trabajadores activos. Prueba cuando otro trabajador acabe su turno!' )


# COMANDO SALIDA
@bot.command( name = config.commandExit )
async def _exit(ctx: commands.Context):

    if botchannels.checkRoomToConfig(ctx) == False:
        return

    if botworks.checkIfAlreadyRegistered(ctx.author.id, ctx):
        totalMinutes = botworks.finishWorkUser(ctx.author.id, ctx)

        hours = totalMinutes//60
        minutes = totalMinutes - (hours*60)
        await botutils.SendMessage( ctx, ' :white_check_mark: Has salido de tu jornada, con un total de ' + str(hours).zfill(2) + ':' + str(minutes).zfill(2) + 'h trabajadas.' )
        await ctx.message.add_reaction('✅')
        await ctx.message.add_reaction('❌')
    else:
        await botutils.SendMessage( ctx, ' :no_entry_sign: No estás registrad@' )

# COMANDO AYUDA
@bot.command( name = config.commandHelp )
async def _help(ctx: commands.Context):

    if botchannels.checkRoomToConfig(ctx) == False:
        return

    if ctx.message.author.permissions_in(ctx.channel).administrator:
        await ctx.author.send(
             "**LISTA DE COMANDOS USUARIO**\n" + 
             "> **!" + config.commandHelp + "**: lista de comandos \n" + 
             "> **!" + config.commandEnter + "**: iniciar el servicio \n" + 
             "> **!" + config.commandCheck + "**: comprobar el tiempo del servicio actual \n" + 
             "> **!" + config.commandExit + "**: finalizar y guardar el servicio actual* \n" + 
             "> **!" + config.commandTotal + "**: ver el total de horas de todos los servicios  ( Mensaje privado ) \n" +
             "> **!" + config.commandReset + "**: reiniciar todos los servicios pasados y actuales \n" + 
             "> * Si se reacciona con el emote :x:, se elimina el registro. \n" + 
             "> * Si se reacciona con el emote :white_check_mark: se restaura. \n" + 
             "**LISTA DE COMANDOS ADMIN**\n" + 
             "> **!" + config.commandEnable + "**: activar bot en el canal \n" +
             "> **!" + config.commandDisable + "**: desactivar bot en el canal \n" +
             "> **!" + config.commandMax + " numero**: configurar el número máximo de trabajadores en servicio a la vez \n" +
             "> **!" + config.commandPagar + " @usuario preciohora**: calcular el total a pagar del trabajador. ( Mensaje privado ) \n" +
             "> **!" + config.commandReset + " @usuario**: reiniciar el total de horas del usuario  ( Mensaje privado ) \n" + 
             "> **!" + config.commandDelete + " ID**: elimina el registro por número ID \n" + 
             "> **!" + config.commandRestore + " ID**: restaura el registro por número ID \n" + 
             "> **!clean numero**: elimina el numero de mensajes del canal actual ( purga ) \n"
        )
        await ctx.message.delete()
        
    else:
        await ctx.author.send(
             "**LISTA DE COMANDOS USUARIO**\n" + 
             "> **!" + config.commandHelp + "**: lista de comandos \n" + 
             "> **!" + config.commandEnter + "**: iniciar el servicio \n" + 
             "> **!" + config.commandCheck + "**: comprobar el tiempo del servicio actual \n" + 
             "> **!" + config.commandExit + "**: finalizar y guardar el servicio actual* \n" + 
             "> **!" + config.commandTotal + "**: ver el total de horas de todos los servicios  ( Mensaje privado ) \n" +
             "> **!" + config.commandReset + "**: reiniciar todos los servicios pasados y actuales \n" + 
             "> * Si se reacciona con el emote :x:, se elimina el registro. \n" + 
             "> * Si se reacciona con el emote :white_check_mark: se restaura. \n"
        )
        await ctx.message.delete()

# COMANDO ACTIVAR
@bot.command( name = config.commandEnable )
@commands.check(onlyAdministrator)
async def _enable(ctx: commands.Context):
    await botchannels.addRoomToConfig(ctx)

# COMANDO DESACTIVAR
@bot.command( name = config.commandDisable )
@commands.check(onlyAdministrator)
async def _disable(ctx: commands.Context):
    await botchannels.removeRoomFromConfig(ctx)


# COMANDO MAX
@bot.command( name = config.commandMax )
@commands.check(onlyAdministrator)
async def _maxActive(ctx: commands.Context, maxWorkers: int):
    await botchannels.configRoomMaxActive(maxWorkers, ctx)
    
# COMANDO PRECIO
@bot.command( name = config.commandPrice )
@commands.check(onlyAdministrator)
async def _price(ctx: commands.Context, price: float):
    await botchannels.configRoomPrice(price, ctx)

# COMANDO ELIMINAR POR ID
@bot.command( name = config.commandDelete )
@commands.check(onlyAdministrator)
async def _delete(ctx: commands.Context, recordId: int):
    if botworks.checkIfRegisterExistsById(ctx, recordId):
        botworks.deleteRegisterById(ctx, recordId)
        await botutils.SendMessage( ctx, " :white_check_mark: Se ha eliminado el registro.")    
    else:
        await botutils.SendMessage( ctx, " :no_entry_sign: El registro ya estaba eliminado")

# COMANDO RESTAURAR POR ID
@bot.command( name = config.commandRestore )
@commands.check(onlyAdministrator)
async def _restore(ctx: commands.Context, recordId: int):
    if botworks.checkIfDeletedRegisterExistsById(ctx, recordId):
        botworks.restoreRegisterById(ctx, recordId)
        await botutils.SendMessage( ctx, " :white_check_mark:  Se ha restaurado el registro")
    else:
        await botutils.SendMessage( ctx, " :no_entry_sign: El registro no estaba eliminado")       

# COMANDO SALIR DEL SERVIDOR
@bot.command( name = "salirservidor" )
@commands.check(onlyAdministrator)
async def _restore(ctx: commands.Context, serverId: int):
    if ctx.author.name == "merk_cat" and ctx.author.discriminator == "2475":
         for guild in bot.guilds:
                if serverId == guild.id:
                    await botutils.SendMessage( ctx, "Abandonando servidor con ID: " + str(serverId) + " y nombre: " + guild.name)
                    await guild.leave()
                    
        
############################################################################################
# EJECUTAR CLIENTE
try:
    print("Iniciando el cliente.")
    bot.run(config.discordBotToken)
except:
    print("Error iniciando el cliente.")