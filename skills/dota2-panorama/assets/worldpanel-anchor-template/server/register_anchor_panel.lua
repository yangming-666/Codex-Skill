-- Reusable server-side snippet for fixed-size worldpanel alignment.
-- Requires libraries/worldpanels.lua

local ANCHOR_WIDTH_BOSS = 320
local ANCHOR_HEIGHT_BOSS = 28
local ANCHOR_WIDTH_ELITE = 220
local ANCHOR_HEIGHT_ELITE = 20

local function ResolveAnchorSize(variant)
    if variant == "elite" then
        return ANCHOR_WIDTH_ELITE, ANCHOR_HEIGHT_ELITE
    end
    return ANCHOR_WIDTH_BOSS, ANCHOR_HEIGHT_BOSS
end

function RegisterAnchorPanel(unit, variant, text)
    if not unit or unit:IsNull() then
        return nil
    end

    local w, h = ResolveAnchorSize(variant)
    local entid = unit:GetEntityIndex()

    return WorldPanels:CreateWorldPanelForAll({
        layout = "file://{resources}/layout/custom_game/worldpanels/anchor_panel.xml",
        entity = unit,
        entityHeight = 100,
        horizontalAlign = "center",
        verticalAlign = "bottom",
        offsetX = 0,
        offsetY = -60,
        data = {
            entity_index = entid,
            variant = variant or "boss",
            text = text or "x1",
            worldpanel_size_mode = "actual",
            worldpanel_fixed_width = w,
            worldpanel_fixed_height = h,
        },
    })
end
