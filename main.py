import os
from keep_alive import keep_alive
import discord.ext
import ast
import json
async def async_exec(stmts, env=None):
    try:
      parsed_stmts = ast.parse(stmts)
  
      fn_name = "_async_exec_f"
  
      fn = f"async def {fn_name}(): pass"
      parsed_fn = ast.parse(fn)
  
      for node in parsed_stmts.body:
          ast.increment_lineno(node)
  
      parsed_fn.body[0].body = parsed_stmts.body
      exec(compile(parsed_fn, filename="<ast>", mode="exec"), env)
  
      return await eval(f"{fn_name}()", env)
    except Exception as e:
        return str(e)
      
def Convert(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct
def is_json_key_present(json, key):
    try:
        buf = json[key]
    except KeyError:
        return False

    return True
client = discord.Client()
@client.event
async def on_ready():
  print("READY")
channels = {}
fr = open("channels.json","r",encoding = "utf-8")
datar = json.loads(fr.read())
fr.close()
if not datar:
  f = open("channels.json","w",encoding = "utf-8")
  json.dump({"channels":{}},f)
  f.close()
@client.event
async def on_message(msg):
  if msg.author != client:
    if msg.content == "?createChannel":
      channel = await msg.guild.create_text_channel('execute-code')
      jsR = open("channels.json","r",encoding = "utf-8")
      chn = json.loads(jsR.read())
      jsR.close()
      jsW = open("channels.json","w",encoding = "utf-8")
      entry = {str(channel.id):channel.id}
      jsW.seek(0)
      chn["channels"].update(entry)
      json.dump(chn,jsW)
      jsW.truncate()
      jsW.close()
    js = open("channels.json")
    data = json.load(js)
    js.close()
    if str(msg.channel.id) in data["channels"]:
      split = msg.content.split("?py ")
      if msg.content.startswith("?py"):
        try:
          if split[1]:
            split[1] = split[1].replace("```py","")
            split[1] = split[1].replace("```","")
            code = split[1]
            value = await async_exec(code)
            try:
              await msg.channel.send(value)
            except:
              await msg.channel.send("Too long of a return value!")
        except:
          await msg.channel.send("""Make sure to add "`" 3 times at the beginning and end """)
      
        
keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)  # Starts the bot
