import db
import config

############################################################################################
# Función para eliminar registros pasados
def checkRoomToConfig(message):

    roomId = message.channel.id
    serverId = message.guild.id

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "SELECT register_id FROM rooms_active WHERE room_id = %s AND server_id = %s ",
        ( str(roomId), str(serverId) )
    )

    return mycursor.rowcount > 0

############################################################################################
# Función para crear sala
async def addRoomToConfig(message):
    if checkRoomToConfig(message) == False:
        roomId = message.channel.id
        serverId = message.guild.id

        mycursor = db.mydb.cursor(buffered=True)
        mycursor.execute("INSERT INTO rooms_active (room_id, server_id) VALUES (%s, %s)", ( str(roomId), str(serverId) ) )

        db.mydb.commit()

        await message.channel.send( '<@' + str(message.author.id) + '> Se ha activado la sala para el registro horario' )

############################################################################################
# Función para eliminar sala
async def removeRoomFromConfig(message):
    if checkRoomToConfig(message):
        roomId = message.channel.id
        serverId = message.guild.id

        mycursor = db.mydb.cursor(buffered=True)
        mycursor.execute("DELETE FROM rooms_active WHERE room_id = %s AND server_id = %s", ( str(roomId), str(serverId) ) )
        db.mydb.commit()

        await message.channel.send('<@' + str(message.author.id) + '> Se han eliminado esta sala para el registro horario' )

############################################################################################
# Función para poner precio registro
async def configRoomPrice(price, message):
    if checkRoomToConfig(message):
        roomId = message.channel.id
        serverId = message.guild.id

        mycursor = db.mydb.cursor(buffered=True)
        mycursor.execute(
            "UPDATE rooms_active SET price = %s WHERE room_id = %s AND server_id = %s ", 
            ( price, roomId, serverId ) 
        )

        db.mydb.commit()

        await message.channel.send( '<@' + str(message.author.id) + '> Se ha cambiado el precio hora a: ' + str(price) )
    else:
         await message.channel.send( '<@' + str(message.author.id) + '> No está configurada la sala. Utiliza primero !' + config.commandEnable )

            
############################################################################################
# Función para coger precio registro
def getRoomPrice(message):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "SELECT price FROM rooms_active WHERE room_id = %s AND server_id = %s ",
        ( message.channel.id, message.guild.id )
    )

    myresult = mycursor.fetchone()
    
    price = myresult[0]

    if price is None :
        return 0
    else:
        return price

############################################################################################
# Función para poner precio registro
async def configRoomMaxActive(maxWorkers, message):
    if checkRoomToConfig(message):
        roomId = message.channel.id
        serverId = message.guild.id

        mycursor = db.mydb.cursor(buffered=True)
        mycursor.execute(
            "UPDATE rooms_active SET max_active = %s WHERE room_id = %s AND server_id = %s ", 
            ( maxWorkers, roomId, serverId ) 
        )

        db.mydb.commit()

        await message.channel.send( '<@' + str(message.author.id) + '> Se ha cambiado el máximo de trabajadores activos a: ' + str(maxWorkers) + '. Para ponerlos ilimitados, puedes usar -1 como número máximo' )
    else:
         await message.channel.send( '<@' + str(message.author.id) + '> No está configurada la sala. Utiliza primero !' + config.commandEnable )
            
############################################################################################
# Función para coger precio registro
def getMaxWorkers(message):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "SELECT max_active FROM rooms_active WHERE room_id = %s AND server_id = %s ",
        ( message.channel.id, message.guild.id )
    )

    myresult = mycursor.fetchone()
    
    maxWorkers = myresult[0]

    if maxWorkers is None :
        return 0
    else:
        return maxWorkers
    
############################################################################################
# Función para coger todas las salas
def getAllActiveRooms():

    mycursor = db.mydb.cursor(buffered=True,dictionary=True)
    mycursor.execute( "SELECT * FROM rooms_active" )

    myresult = mycursor.fetchall()
    
    return myresult

############################################################################################
# Función para coger todas las salas
async def sendMessageToAllRooms(bot, message):
    
    channelList = getAllActiveRooms()
    
    for ch in channelList:
        channel = bot.get_channel( int(ch["room_id"]) )
        await channel.send(message)