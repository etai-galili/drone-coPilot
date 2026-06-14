SYSTEM_PROMPT = (
    "You are AVATA CO-PILOT, an AI field assistant for DJI Avata drone operators.\n"
    "Always respond in English only, regardless of input language.\n"
    "Keep answers to 1-3 sentences unless a numbered checklist is explicitly requested.\n"
    "Never invent specifications — only state facts from the provided context.\n"
    "If uncertain: respond with \"Check the manual — I cannot confirm this.\"\n"
    "For emergencies, lead with the action: \"LAND IMMEDIATELY\" or \"ACTIVATE RTH NOW\".\n"
    "Prioritize operator safety and bystander safety above all else.\n"
    "Format checklists as numbered steps."
)

PREFLIGHT_PROMPTS = {
    "Indoor Recon": (
        "Generate a numbered pre-flight checklist for indoor reconnaissance with the DJI Avata. "
        "Include checks for obstacle avoidance, propeller guards, and confined-space safety."
    ),
    "Outdoor Recon": (
        "Generate a numbered pre-flight checklist for outdoor reconnaissance with the DJI Avata. "
        "Include GPS lock, wind check, and airspace verification."
    ),
    "FPV Freestyle": (
        "Generate a numbered pre-flight checklist for FPV freestyle flying with the DJI Avata. "
        "Include motor check, props, goggles link, and clear flight zone."
    ),
    "Mapping": (
        "Generate a numbered pre-flight checklist for a mapping mission with the DJI Avata. "
        "Include battery level, SD card, GPS, and return-to-home altitude."
    ),
    "SAR": (
        "Generate a numbered pre-flight checklist for a Search and Rescue mission with the DJI Avata. "
        "Include communication check, battery reserve, and handoff procedure."
    ),
}


def build_prompt(system: str, user: str, context: str = "") -> str:
    context_block = f"\nCONTEXT:\n{context}\n" if context else ""
    return (
        f"<|im_start|>system\n{system}{context_block}<|im_end|>\n"
        f"<|im_start|>user\n{user}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )
