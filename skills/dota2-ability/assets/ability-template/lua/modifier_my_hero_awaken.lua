-- Awakening override template
LinkLuaModifier("modifier_my_hero_my_ability_awakening", "hero/hero_my_hero/modifier_my_hero_awaken", LUA_MODIFIER_MOTION_NONE)

modifier_my_hero_my_ability_awakening = class(modifier_base_awakening)

function modifier_my_hero_my_ability_awakening:OnCreated()
    self.awaken_values = {
        damage = true,
        radius = true,
    }
end

function modifier_my_hero_my_ability_awakening:GetModifierOverrideAbilitySpecialValue(params)
    if params.ability_special_value == "damage" then
        local base = params.ability:GetLevelSpecialValueNoOverride("damage", params.ability_special_level)
        local difficulty = GameRules:GetCustomGameDifficulty() or 0
        return base + (difficulty * 25)
    end
    if params.ability_special_value == "radius" then
        local base = params.ability:GetLevelSpecialValueNoOverride("radius", params.ability_special_level)
        return base + 50
    end
end
