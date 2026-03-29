# Frame Extension: MITRE ATT&CK

This extension provides the full vocabulary of [MITRE ATT&CK®](https://attack.mitre.org/) techniques and sub-techniques for use in Frame.

**Namespace:** `mitre.attack`
**Extends:** `Domain.Security`

## Coverage
Includes techniques from:
- Enterprise ATT&CK
- Mobile ATT&CK
- ICS ATT&CK

## Usage
Add `mitre.attack` tags to your Frame to specify the exact security technique being discussed.

```yaml
Frame:
  Domain.Security
  Object.Event
  mitre.attack:T1059.001  # PowerShell
```

## Source
This extension is generated directly from the official MITRE STIX 2.1 data.

- **Index:** [MITRE ATT&CK STIX Data](https://github.com/mitre-attack/attack-stix-data)
- **More Info:** [ATT&CK Data & Tools](https://attack.mitre.org/resources/attack-data-and-tools/)

To regenerate this extension with the latest data, run the Frame extension generator.
