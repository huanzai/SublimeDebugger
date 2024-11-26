require "debugger":start "127.0.0.1:12306":setup_patch():event "wait"

local a = 1
local b = 2

local t = {
    {a = 1, b = 2},
    {a = 1, b = 2},
    {a = 1, b = 2},
    {a = 1, b = 2},

    aa = 3,
    bb = 4,
    cc = {
        a=1,b=3
    },
}

local t2 = {
    a = {11,22},
    b = {11,22},
}

local function foo()
    return a + b
end

local c = foo()

print(c)