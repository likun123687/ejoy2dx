local audio = require "ejoy2dx.Liekkas.audio"

local M = {}
local sound_group = audio:create_group(16)


function M:load(file_path)
  return audio:load(file_path)
end


function M:unload(file_path)
  return audio:unload(file_path)
end

function M:play(file_path, loop, pitch, gain)
  local handle  = sound_group:add(file_path, loop, pitch, gain)
  if not handle then
  	return
  end
  sound_group:play(handle)
  return handle
end

function M:open()
  return sound_group:open()
end

function M:close()
  return sound_group:close()
end

return M