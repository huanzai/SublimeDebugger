require "debugger":start "127.0.0.1:12306":setup_patch():event "wait"

local a = 1
local b = 2

local function foo()
    return a + b
end

local c = foo()

print(c)