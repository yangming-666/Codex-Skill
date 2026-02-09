-- Base ability skeleton
my_hero_my_ability = class({})

LinkLuaModifier("modifier_my_hero_my_ability", "hero/hero_my_hero/my_hero_my_ability", LUA_MODIFIER_MOTION_NONE)

function my_hero_my_ability:GetIntrinsicModifierName()
    return "modifier_my_hero_my_ability"
end

function my_hero_my_ability:OnSpellStart()
    if not IsServer() then return end
    local caster = self:GetCaster()
    local target = self:GetCursorTarget()
    if not caster or caster:IsNull() then return end

    -- TODO: implement ability logic
end

modifier_my_hero_my_ability = class({})

function modifier_my_hero_my_ability:IsHidden() return true end
function modifier_my_hero_my_ability:IsPurgable() return false end

function modifier_my_hero_my_ability:DeclareFunctions()
    return {
        MODIFIER_EVENT_ON_ATTACK_LANDED,
    }
end

function modifier_my_hero_my_ability:OnAttackLanded(params)
    if not IsServer() then return end
    if params.attacker ~= self:GetParent() then return end

    -- TODO: implement passive trigger
end
