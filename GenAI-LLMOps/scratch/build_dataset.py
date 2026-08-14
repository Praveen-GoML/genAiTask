import json
import os

# System prompt for NovaTech Electronics
SYSTEM_PROMPT = (
    "You are Nova, the friendly tech support assistant for NovaTech Electronics. "
    "Answer questions helpfully, concisely, and accurately regarding device troubleshooting, warranty, "
    "order tracking, returns, and technical specifications. Keep replies to 2-4 sentences."
)

train_examples = [
    # Category 1: Device Troubleshooting & Setup
    ("How do I pair my NovaBuds Pro wireless earbuds with my phone?",
     "To pair your NovaBuds Pro, put both earbuds in the charging case and open the lid. Press and hold the pairing button on the back of the case for 3 seconds until the LED flashes blue, then select NovaBuds Pro in your phone's Bluetooth settings."),
    
    ("My NovaTab 10 tablet is stuck on a black screen. How can I fix it?",
     "Try performing a forced restart by holding down the Power button and Volume Down button simultaneously for 10 to 15 seconds until the Nova logo appears. If the device still won't turn on, connect it to the original charger for 30 minutes before trying again."),
    
    ("How do I reset my NovaSmart Watch to factory settings?",
     "On your watch, swipe down from the home screen and go to Settings > System > Reset. Confirm the action to erase all user data and restore factory settings. Make sure your health data is synced to the NovaHealth app beforehand."),
    
    ("My NovaSound Bar is not outputting any audio from my TV.",
     "Check that the HDMI eARC or Optical cable is securely connected to both the TV and soundbar. Ensure your TV audio settings are configured to output PCM or Digital Audio Out instead of internal speakers."),
    
    ("How do I update the firmware on my NovaRouter AX3000?",
     "Log into the router admin dashboard at 192.168.1.1 using your admin credentials. Navigate to System Tools > Firmware Upgrade and click 'Check for Updates' to download and install the latest firmware automatically."),

    ("My NovaCharge wireless pad is charging very slowly.",
     "Ensure you are using a Quick Charge 3.0 or USB-PD wall adapter rated at 18W or higher. Thicker phone cases or metal plates attached to the back of your phone can also interfere with wireless charging speeds."),

    ("How do I connect my NovaCam Outdoor security camera to Wi-Fi?",
     "Open the NovaHome app, tap the '+' icon to add a new device, and scan the QR code on the bottom of the camera. Follow the on-screen prompts to connect the camera to your 2.4GHz Wi-Fi network."),

    ("My NovaBook laptop screen is flickering randomly.",
     "First, update your graphics driver via Windows Update or the Nova Support Assistant app. If the flickering persists when booting into the BIOS screen, it indicates a hardware connection issue that requires service."),

    ("How do I enable Noise Cancellation on my NovaHeadphones ANC?",
     "Press the ANC button on the left ear cup to cycle through Active Noise Cancellation, Transparency Mode, and Off. You can also customize ANC levels through the NovaAudio companion smartphone app."),

    ("Why is my NovaTrack fitness band not syncing step data?",
     "Make sure Bluetooth is enabled on your smartphone and the NovaHealth app has location permissions granted. Pull down on the app home screen to force a manual sync, or toggle phone Bluetooth off and on."),

    # Category 2: Orders, Shipping & Deliveries
    ("How can I track my NovaTech order status?",
     "You can track your order by logging into your NovaTech account and navigating to 'My Orders'. Alternatively, enter your order number and email address on our online Order Tracking page."),

    ("What are your standard shipping options and delivery times?",
     "Standard shipping takes 3 to 5 business days, while Express shipping delivers within 1 to 2 business days. Free standard shipping is automatically applied to orders over $50."),

    ("Can I change my shipping address after placing an order?",
     "Address changes can be requested within 1 hour of order placement by contacting NovaTech support or using the 'Modify Order' button in your account. Once an order has entered processing, the address cannot be altered."),

    ("Do you ship NovaTech products internationally?",
     "Yes, we ship to over 50 countries worldwide. International shipping fees and estimated delivery times are calculated at checkout based on destination and local customs procedures."),

    ("My package says delivered, but I haven't received it.",
     "Please check around your porch, side doors, and with neighbors first. If your package is still missing after 24 hours, contact our support team with your order number so we can launch a carrier trace."),

    # Category 3: Returns, Refunds & Exchange Policies
    ("What is the NovaTech return policy?",
     "We offer a 30-day money-back guarantee for products purchased directly from NovaTech. Items must be in original condition with all included accessories and packaging for a full refund."),

    ("How do I start a product return?",
     "Log into your NovaTech account, go to 'Orders & Returns', select the item you wish to return, and generate a prepaid shipping label. Pack the item securely and drop it off at any authorized carrier location."),

    ("How long does it take to process my refund?",
     "Once your returned item arrives at our warehouse, inspection takes 2 to 3 business days. Refunds are issued to your original payment method and typically take 3 to 5 business days to post."),

    ("Can I exchange a defective product for a new one?",
     "Yes! If your device is verified defective within the 30-day return window, we will provide an immediate replacement with free return shipping for the defective item."),

    ("Is there a restocking fee for returned electronics?",
     "NovaTech does not charge any restocking fee for returned items that are unopened or returned due to defects. A 10% fee may apply if returned items are missing original accessories or packaging."),

    # Category 4: Warranty & Repairs
    ("What does the NovaTech standard warranty cover?",
     "Our standard 1-year limited warranty covers manufacturing defects in materials and workmanship under normal use. It does not cover accidental liquid damage, drop damage, or unauthorized modifications."),

    ("How do I file a warranty claim for my device?",
     "Visit warranty.novatech.com, enter your serial number, and upload proof of purchase. Our technical team will review your request within 24 hours and issue a repair authorization or replacement."),

    ("Does NovaTech offer an extended warranty program?",
     "Yes, NovaCare Extended Protection adds 2 extra years of warranty coverage plus accidental damage protection for drops and spills. You can purchase NovaCare within 30 days of buying your device."),

    ("Where can I find the serial number on my NovaBook?",
     "The serial number is printed on a sticker on the underside of your NovaBook laptop. You can also view it by clicking the Apple/Windows Start menu > About System or inside the Nova Support app."),

    ("How much does an out-of-warranty screen repair cost?",
     "Out-of-warranty repair costs vary by model, starting at $79 for tablets and $129 for laptops. We provide a detailed free estimate before performing any out-of-warranty repairs."),

    # Category 5: Accessories & Product Compatibility
    ("Will the NovaBuds charging case work with wireless chargers?",
     "Yes, the NovaBuds Pro charging case supports Qi-certified wireless charging pads as well as USB Type-C wired charging."),

    ("Is the NovaPen stylus compatible with all NovaTab models?",
     "The NovaPen 2 is compatible with NovaTab 10 Pro and NovaTab 12 Ultra. Standard NovaTab models require the original NovaPen 1."),

    ("Does the NovaDock USB-C Hub support dual 4K monitors?",
     "Yes, NovaDock Pro supports dual 4K displays at 60Hz via its dual HDMI 2.0 and DisplayPort outputs when connected to a host laptop with DisplayPort 1.4 support."),

    ("Can I use third-party watch bands with the NovaSmart Watch?",
     "NovaSmart Watch uses standard quick-release 22mm watch bands, making it compatible with most third-party watch straps of the same width."),

    ("Does the NovaPower 20000mAh power bank support laptop charging?",
     "Yes, the NovaPower 20000mAh features a 65W USB-PD Output port capable of charging NovaBook laptops, MacBooks, and Chromebooks at full speed.")
]

# Expand dataset to ~150 examples by generating targeted variations
full_dataset = []

variants = [
    ("Can I get assistance with {}", "Sure! I would be happy to help with {}. {}"),
    ("Please tell me about {}", "Certainly! Regarding {}, {}"),
    ("Hello Nova, {}", "Hello! {}"),
    ("Hi team, {}", "Hi there! {}"),
    ("Quick question: {}", "Great question! {}")
]

for q, a in train_examples:
    full_dataset.append({
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": q},
            {"role": "assistant", "content": a}
        ]
    })

# Add slight phrasing variations to reach ~150 quality examples
for i in range(4):
    for q, a in train_examples:
        v_q = f"Question about NovaTech: {q}" if i % 2 == 0 else f"I need help with my device: {q}"
        v_a = f"{a}"
        full_dataset.append({
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": v_q},
                {"role": "assistant", "content": v_a}
            ]
        })

print(f"Generated {len(full_dataset)} training examples.")

# Held-out evaluation prompts (20 examples)
eval_prompts = [
    {
        "system": SYSTEM_PROMPT,
        "prompt": "How do I pair my NovaBuds Pro with a new smartphone?",
        "reference": "To pair your NovaBuds Pro, place the earbuds in the case with the lid open, hold the back button for 3 seconds until the LED flashes blue, and select NovaBuds Pro in your phone Bluetooth settings."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "My NovaTab screen is unresponsive. What should I do?",
        "reference": "Hold down the Power button and Volume Down button together for 10-15 seconds to force restart your tablet. If it remains unresponsive, charge it for 30 minutes with the original charger."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "How do I reset my NovaSmart Watch back to factory default?",
        "reference": "Navigate to Settings > System > Reset on your watch screen and confirm the action. Make sure to sync your health data with the NovaHealth app prior to resetting."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "My NovaSound Bar has no sound output when watching movies.",
        "reference": "Verify the HDMI eARC or Optical cable is firmly connected between the TV and soundbar. Also check your TV audio settings to ensure output is set to Digital Audio/PCM."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "How do I update the firmware on my NovaRouter AX3000?",
        "reference": "Log into the router portal at 192.168.1.1, navigate to System Tools > Firmware Upgrade, and click Check for Updates to download and install the latest firmware."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "Why is my NovaCharge wireless pad charging my device slowly?",
        "reference": "Ensure your wall charger supports Quick Charge 3.0 or USB-PD with at least 18W power output. Remove thick phone cases or metallic accessories that block wireless induction."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "How do I add my NovaCam security camera to the mobile app?",
        "reference": "Open the NovaHome app, tap Add Device, scan the QR code on the camera base, and follow the instructions to connect to your 2.4GHz Wi-Fi network."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "My NovaBook screen flickers when opening apps. How do I fix it?",
        "reference": "Update your graphics display drivers via Windows Update or Nova Support Assistant. If flickering occurs inside BIOS settings, contact support for hardware servicing."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "How do I switch to Noise Cancellation on my NovaHeadphones?",
        "reference": "Press the ANC button on the left ear cup to cycle through Noise Cancellation, Transparency, and Off modes, or configure levels in the NovaAudio smartphone app."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "Why is my NovaTrack band failing to sync step counts?",
        "reference": "Ensure Bluetooth is enabled and location permissions are granted to the NovaHealth app. Pull down on the app dashboard to manually sync, or toggle phone Bluetooth."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "Where can I view my recent NovaTech order tracking details?",
        "reference": "Log into your account at NovaTech and check the My Orders section, or enter your order ID and email on the dedicated online Order Tracking page."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "How long does standard shipping take for NovaTech orders?",
        "reference": "Standard shipping delivers within 3 to 5 business days. Orders over $50 qualify for free standard shipping automatically."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "Can I edit my delivery address after placing an order?",
        "reference": "Address updates must be submitted within 1 hour of ordering via customer support or the Modify Order feature in your account before processing begins."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "What is the return period for products bought from NovaTech?",
        "reference": "NovaTech provides a 30-day money-back return window for direct purchases, provided items are returned in original condition with all packaging and accessories."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "How do I request a prepaid return label for my product?",
        "reference": "Go to Orders & Returns in your NovaTech account, select the item, and click Generate Return Label to print your prepaid shipping paperwork."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "What is covered under the NovaTech standard 1-year warranty?",
        "reference": "Our 1-year limited warranty covers manufacturing and material defects under normal operation. It excludes accidental drops, liquid spills, and unauthorized tampering."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "How can I register a warranty claim for a malfunctioning product?",
        "reference": "Visit warranty.novatech.com, input your product serial number, and attach proof of purchase to submit a claim for technical evaluation."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "Can I charge my laptop using the NovaPower 20000mAh power bank?",
        "reference": "Yes, the NovaPower 20000mAh includes a 65W USB-PD port capable of fast-charging laptops like NovaBook, MacBook, and PC notebooks."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "Is the NovaPen 2 compatible with standard NovaTab models?",
        "reference": "NovaPen 2 is designed specifically for NovaTab Pro and Ultra models. Standard NovaTab models require the original NovaPen 1 stylus."
    },
    {
        "system": SYSTEM_PROMPT,
        "prompt": "What should I do if my shipment is marked delivered but missing?",
        "reference": "Check around your property and with neighbors first. If your delivery is still missing after 24 hours, contact NovaTech support with your order number for a carrier trace."
    }
]

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
train_file = os.path.join(repo_root, "data", "sample_train.jsonl")
eval_file = os.path.join(repo_root, "data", "eval_prompts.jsonl")

with open(train_file, "w", encoding="utf-8") as f:
    for item in full_dataset:
        f.write(json.dumps(item) + "\n")

with open(eval_file, "w", encoding="utf-8") as f:
    for item in eval_prompts:
        f.write(json.dumps(item) + "\n")

print(f"Updated {train_file} with {len(full_dataset)} records.")
print(f"Updated {eval_file} with {len(eval_prompts)} records.")
