
local log = require("log")
local Api = require("coreApi")
local json = require("json")
local http = require("http")
-- CurrentQQ 当前操作的QQ号 /funcName 欲调用LuaApi函数名 ／data  组装Json数据
function Api_LuaCaller(CurrentQQ, funcName, data)
    str = string.format("Api_LuaCaller FuncName %s\n", funcName)
    log.info("%s", str)
    local luaResp = nil
    local switch = {
        ["MagicCgiCmd"] = function()
            return Api.Api_MagicCgiCmd(CurrentQQ, data)
        end
    }
    local fSwitch = switch[funcName] --switch func
    if fSwitch then --key exists
        luaResp = fSwitch() --do func
    else --key not found
        luaResp = Api.Api_CallFunc(CurrentQQ, funcName, data)
    end
    return luaResp
end
