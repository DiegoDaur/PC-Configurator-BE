from model.compatibility_rule import CompatibilityRule
from repository import compatibility_rule_repository, component_repository
from exception.app_exception import AppException


def get_all():
    return compatibility_rule_repository.get_all()


def get_by_id(rule_id):
    rule = compatibility_rule_repository.get_by_id(rule_id)
    if rule is None:
        raise AppException("Regola di compatibilità non trovata!", 404)
    return rule


def create(data):
    _validate_rule(data)

    id_a = int(data["component_a_id"])
    id_b = int(data["component_b_id"])

    if component_repository.get_by_id(id_a) is None:
        raise AppException(f"Componente A (id={id_a}) non trovato!", 404)
    if component_repository.get_by_id(id_b) is None:
        raise AppException(f"Componente B (id={id_b}) non trovato!", 404)

    existing = compatibility_rule_repository.get_rule_between(id_a, id_b)
    if existing:
        raise AppException(f"Esiste già una regola tra questi due componenti (id={existing.id})!", 409)

    new_rule = CompatibilityRule(
        id=None,
        component_a_id=id_a,
        component_b_id=id_b,
        is_compatible=bool(data.get("is_compatible", True)),
        reason=data.get("reason"),
    )

    return compatibility_rule_repository.create(new_rule)


def update(rule_id, data):
    if compatibility_rule_repository.get_by_id(rule_id) is None:
        raise AppException("Regola di compatibilità non trovata!", 404)
    return compatibility_rule_repository.update(rule_id, data)


def delete_by_id(rule_id):
    if compatibility_rule_repository.get_by_id(rule_id) is None:
        raise AppException("Regola di compatibilità non trovata!", 404)
    compatibility_rule_repository.delete_by_id(rule_id)


def check_compatibility(component_ids):
    if not component_ids or len(component_ids) < 2:
        return {"is_compatible": True, "issues": [], "ok_rules": []}

    issues = []
    ok_rules = []

    ids = list(set(component_ids))
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            rule = compatibility_rule_repository.get_rule_between(ids[i], ids[j])
            if rule:
                entry = {
                    "component_a_id": ids[i],
                    "component_b_id": ids[j],
                    "is_compatible":  rule.is_compatible,
                    "reason":         rule.reason,
                }
                if rule.is_compatible:
                    ok_rules.append(entry)
                else:
                    issues.append(entry)

    return {
        "is_compatible": len(issues) == 0,
        "issues":        issues,
        "ok_rules":      ok_rules,
    }


def get_compatible_components(component_id, target_category):
    all_in_category = component_repository.get_by_category(target_category)
    rules = compatibility_rule_repository.get_rules_for_component(component_id)

    incompatible_ids = set()
    for rule in rules:
        if not rule.is_compatible:
            other_id = rule.component_b_id if rule.component_a_id == component_id else rule.component_a_id
            incompatible_ids.add(other_id)

    return [c for c in all_in_category if c.id not in incompatible_ids]


def _validate_rule(data):
    for campo in ["component_a_id", "component_b_id"]:
        if campo not in data:
            raise AppException(f"Campo '{campo}' obbligatorio!", 400)

    if int(data["component_a_id"]) == int(data["component_b_id"]):
        raise AppException("Un componente non può avere una regola con sé stesso!", 400)
