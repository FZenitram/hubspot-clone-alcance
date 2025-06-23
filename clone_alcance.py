import os, time
from hubspot import HubSpot
from hubspot.crm.properties import ApiException

TOKEN = os.getenv("HUBSPOT_PRIVATE_APP_TOKEN")
client = HubSpot(access_token=TOKEN)
OBJECT_TYPE = "alcance"

def clone_properties():
    resp = client.crm.properties.core_api.get_all(OBJECT_TYPE)
    props = resp.results
    print(f"Encontradas {len(props)} propiedades en '{OBJECT_TYPE}'.")
    for p in props:
        new_name  = f"{p.name}_copy"
        new_label = f"{p.label} Copia"
        body = {
            "name":         new_name,
            "label":        new_label,
            "type":         p.type,
            "fieldType":    p.field_type,
            "groupName":    p.group_name,
            "options":      p.options or [],
            "displayOrder": p.display_order,
            "description":  p.description or "",
            "formField":    p.form_field,
        }
        try:
            client.crm.properties.core_api.create(OBJECT_TYPE, body)
            print(f"✅ {p.name} → {new_name}")
        except ApiException as e:
            print(f"❌ Error en {p.name}: {e.status} {e.body}")
        time.sleep(0.1)

if __name__ == "__main__":
    clone_properties()
