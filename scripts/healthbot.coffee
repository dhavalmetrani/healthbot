# Description
#   A hubot script that does the things
#
# Configuration:
#   HUBOT_RUN="bash/handler"
#   PYTHON_EXECUTABLE="/usr/bin/python"
#   BASH_EXECUTABLE="/bin/bash"
#   PYTHON_SCRIPT_FOLDER=""
# Commands:
#  help - Lists the available commands.
#
# Notes:
#   <optional notes required for the script>
#
# Author:
#   Dhaval Metrani

##########################################################
# Check if handler exists and set default handler
##########################################################
fs = require("fs")

process.env.HUBOT_RUN = "bash/handler" if not process.env.HUBOT_RUN
if not fs.existsSync(process.env.HUBOT_RUN)
  console.log process.env.HUBOT_RUN+" not found in hubot working dir... Defaulting to example handler at "+__dirname+"/../bash/handler"
  process.env.HUBOT_RUN = __dirname+"/../bash/handler"
process.env.PYTHON_SCRIPT_FOLDER = __dirname+"/../src/python/" if not process.env.PYTHON_SCRIPT_FOLDER
process.env.PYTHON_EXECUTABLE = "/usr/bin/python" if not process.env.PYTHON_EXECUTABLE
process.env.BASH_EXECUTABLE = "/usr/bash" if not process.env.BASH_EXECUTABLE

##########################################################

##########################################################
# module exports
##########################################################
module.exports = (robot) ->
  fs = require 'fs'
  fs.exists __dirname+'/logs/', (exists) ->
    if exists
      console.log "Log folder exists..."
    else
      fs.mkdir __dirname+'/logs/', (error) ->
        unless error
          console.log "Log folder created..."
        else
          console.log "Could not create logs directory: #{error}"
##########################################################

  ##########################################################
  # Run command:
  ##########################################################
  run_cmd = (cmd, args, envs, cb ) ->
    console.log "Running command: "+cmd+" "+args
    spawn = require("child_process").spawn
    opts =
        env: envs
    child = spawn(cmd, args, opts)

    child.stdout.on "data", (buffer) -> cb buffer.toString()
    child.stderr.on "data", (buffer) -> cb buffer.toString()
  ##########################################################


  ##########################################################
  # Run command:
  ##########################################################
  robot.respond "/.*/i", (res) ->

    cmd = process.env.PYTHON_EXECUTABLE

    # Copy environment variables to child process
    envs = {}
    envs[key.toUpperCase()] = value for key, value of process.env
    envs["HUBOT_USER_" + key.toUpperCase()] = value for key, value of res.envelope.user

    # input = res.match[0]
    input_array = res.match[0].split /\s+/
    # bot_name = input_array[0].toLowerCase()
    args = input_array[1..]
    input = input_array[1..].toString()

    # command = args[0].toLowerCase()
    command = process.env.PYTHON_SCRIPT_FOLDER + "main.py"
    # Insert at index 0 without deleting any item.
    args.splice(0, 0, command);

    room = res.message.room

    console.log "Input: " + input.replace(/\,/g, " ")
    # res.send "*Input:* `" + input.replace(/\,/g, " ") + "`. Processing. Will post `" + room + "` once i get the results..."
    res.send "*Input:* `" + input.replace(/\,/g, " ") + "`. Processing..."
    console.log args[0]
    # res.send args[0]
    # console.log args[0]

    fs = require 'fs'
    fs.exists args[0], (exists) ->
      if exists
        console.log "Command exists: " + args[0]
        run_cmd cmd, args, envs, (text) ->
          console.log text
          res.reply text
      else
        console.log "The Command specified is not available: " + command + "."
        res.reply "The Command specified is not available: `" + command + "`."
        # args[0] = process.env.PYTHON_SCRIPT_FOLDER + "help.py"
        # run_cmd cmd, args, envs, (text) ->
        #   console.log text
        #   res.reply text


  ##########################################################
