import db
import botutils


############################################################################################
############################################################################################
############################################################################################
# Función para eliminar registros pasados
async def deleteAllRegistersFromUser(userId, message):

    totalMinutes = checkTotalUserTime(userId, message)
    hours = totalMinutes//60
    minutes = totalMinutes - (hours*60)

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "UPDATE work_registers SET deleted = true WHERE user_id = %s AND room_id = %s AND server_id = %s AND deleted = false",
        (userId, message.channel.id, message.guild.id)
    )
    db.mydb.commit()

    await botutils.SendMessage( message, 'Se han eliminado tus ' + str(mycursor.rowcount) + ' registros. Tenías un total de ' + str(hours).zfill(2) + ':' + str(minutes).zfill(2) + 'h trabajadas.' )

############################################################################################
# Función para ver la suma total de horas
def checkTotalUserTime(userId, message):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "SELECT SUM(total_minutes) FROM work_registers WHERE user_id = %s AND total_minutes > 0 AND room_id = %s AND server_id = %s AND deleted = false",
        (userId, message.channel.id, message.guild.id )
    )
    myresult = mycursor.fetchone()
    
    totalMinutes = myresult[0]

    if totalMinutes is None :
        return 0
    else:
        return totalMinutes

############################################################################################
# Función para ver la suma total de horas
def checkTotalUserTimeExtended(userId, message):

    mycursor = db.mydb.cursor(buffered=True,dictionary=True)
    mycursor.execute(
        "SELECT register_id, time_created, time_finished, total_minutes FROM work_registers WHERE user_id = %s AND total_minutes > 0 AND room_id = %s AND server_id = %s AND deleted = false",
        (userId, message.channel.id, message.guild.id )
    )
    myresult = mycursor.fetchall()
    returnText = "`"
    i = 0
    for row in myresult:
        
        if i > 25:
            returnText = returnText + "... Había más mensajes pero se ha limitado a 30. Sorry :( "
            return returnText
        else:
            hours = row["total_minutes"]//60
            minutes = row["total_minutes"] - (hours*60)
            returnText = returnText + " 🔗 ID " + str(row["register_id"]).ljust(4, " ") + ""
            returnText = returnText + " 📅" + row["time_created"].strftime("%d/%m %H:%Mh") + " ▶ " + row["time_finished"].strftime("%d/%m %H:%Mh")
            returnText = returnText + " ⏱" + str(hours).zfill(2) + ':' + str(minutes).zfill(2) + "  "
            returnText = returnText + "\n"
        
        i = i+1
    returnText = returnText + "`"
    return returnText
        

############################################################################################
# Función para ver la diferencia de tiempo entre la entrada y la salida
def checkSessionUserTime(userId, message):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "SELECT time_created, NOW() FROM work_registers WHERE user_id = %s AND room_id = %s AND server_id = %s AND time_finished IS NULL AND deleted = false",
        (userId, message.channel.id, message.guild.id)
    )
    myresult = mycursor.fetchone()

    dateCurrent = myresult[1]
    dateStored = myresult[0]

    dateDifference = dateCurrent - dateStored

    days, seconds = dateDifference.days, dateDifference.seconds

    totalHours = days * 24 + seconds // 3600
    totalMinutes = ((seconds % 3600) // 60) + (totalHours * 60)

    return totalMinutes

############################################################################################
# Función para guardar las horas
def finishWorkUser(userId, message):
    
    totalMinutes = checkSessionUserTime(userId, message)

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "UPDATE work_registers SET time_finished = NOW(), total_minutes = %s, finish_message_id = %s WHERE user_id = %s AND room_id = %s AND server_id = %s AND time_finished IS NULL AND deleted = false",
        (totalMinutes, message.message.id, userId, message.channel.id, message.guild.id)
    )
    db.mydb.commit()

    return totalMinutes

############################################################################################
# Función para comprobar si ya está registrado el usuario
def checkIfAlreadyRegistered(userId, message):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "SELECT register_id FROM work_registers WHERE user_id = %s AND room_id = %s AND server_id = %s AND time_finished IS NULL AND deleted = false",
        (userId, message.channel.id, message.guild.id)
    )

    return mycursor.rowcount > 0

############################################################################################
# Función para comprobar si ya está registrado el usuario
def checkIfRegisterExists(message):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "SELECT register_id FROM work_registers WHERE user_id = %s AND finish_message_id = %s AND room_id = %s AND server_id = %s AND deleted = false",
        (message.author.id, message.id, message.channel.id, message.guild.id)
    )

    return mycursor.rowcount > 0

############################################################################################
# Función para comprobar si ya está registrado el usuario
def checkIfRegisterExistsById(message, registerId):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "SELECT register_id FROM work_registers WHERE user_id = %s AND register_id = %s AND room_id = %s AND server_id = %s AND deleted = false",
        (message.author.id, registerId, message.channel.id, message.guild.id)
    )

    return mycursor.rowcount > 0

############################################################################################
# Función para comprobar si ya está registrado el usuario
def checkIfDeletedRegisterExists(message):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "SELECT register_id FROM work_registers WHERE user_id = %s AND finish_message_id = %s AND room_id = %s AND server_id = %s AND deleted = true AND deleted_manually = true",
        (message.author.id, message.id, message.channel.id, message.guild.id)
    )

    return mycursor.rowcount > 0

############################################################################################
# Función para comprobar si ya está registrado el usuario
def checkIfDeletedRegisterExistsById(message, registerId):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "SELECT register_id FROM work_registers WHERE user_id = %s AND register_id = %s AND room_id = %s AND server_id = %s AND deleted = true AND deleted_manually = true",
        (message.author.id, registerId, message.channel.id, message.guild.id)
    )

    return mycursor.rowcount > 0

############################################################################################
# Función para comprobar si ya está registrado el usuario
def restoreRegisterByMessage(message):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "UPDATE work_registers SET deleted = false, deleted_manually = false WHERE user_id = %s AND finish_message_id = %s AND room_id = %s AND server_id = %s AND deleted = true AND deleted = true",
        (message.author.id, message.id, message.channel.id, message.guild.id)
    )
    db.mydb.commit()

    return

############################################################################################
# Función para comprobar si ya está registrado el usuario
def restoreRegisterById(message, registerId):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "UPDATE work_registers SET deleted = false, deleted_manually = false WHERE user_id = %s AND register_id = %s AND room_id = %s AND server_id = %s AND deleted = true AND deleted = true",
        (message.author.id, registerId, message.channel.id, message.guild.id)
    )
    db.mydb.commit()

    return

############################################################################################
# Función para comprobar si ya está registrado el usuario
def deleteRegisterByMessage(message):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "UPDATE work_registers SET deleted = true, deleted_manually = true WHERE user_id = %s AND finish_message_id = %s AND room_id = %s AND server_id = %s AND deleted = false",
        (message.author.id, message.id, message.channel.id, message.guild.id)
    )
    db.mydb.commit()

    return

############################################################################################
# Función para comprobar si ya está registrado el usuario
def deleteRegisterById(message, registerId):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "UPDATE work_registers SET deleted = true, deleted_manually = true WHERE user_id = %s AND register_id = %s AND room_id = %s AND server_id = %s AND deleted = false",
        (message.author.id, registerId, message.channel.id, message.guild.id)
    )
    db.mydb.commit()

    return

############################################################################################
# Función para registrar un usuario
def registerWorkUser(userId, message):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "INSERT INTO work_registers (user_id, room_id, server_id, start_message_id, username) VALUES (%s, %s, %s, %s, %s)", 
        (userId, message.channel.id, message.guild.id, message.message.id, ascii(message.author.display_name))
    )
    db.mydb.commit()

    return mycursor.lastrowid

############################################################################################
# Función para coger los trabajadores activos
def getActiveWorkers(message):

    mycursor = db.mydb.cursor(buffered=True)
    mycursor.execute(
        "SELECT COUNT(user_id) FROM work_registers WHERE time_finished IS NULL AND room_id = %s AND server_id = %s AND deleted = false", 
        (message.channel.id, message.guild.id)
    )
    myresult = mycursor.fetchone()
    
    if mycursor.rowcount > 0:
        return myresult[0]
    else:
        return 0
    
