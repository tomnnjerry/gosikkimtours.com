"""Policy pages. DRAFTS for legal review: every [BRACKETED] value must be confirmed before launch.

Each policy: title, summary (plain-English box at the top), sections [(heading, [paragraphs] | {"list": [...]})].
"""
from collections import OrderedDict

UPDATED = "[DATE OF LEGAL REVIEW]"

POLICIES = OrderedDict()

POLICIES["refund-and-cancellation"] = {
    "title": "Refund and cancellation policy",
    "nav": "Refunds and cancellations",
    "summary": "If you cancel, what you get back depends on how many days before departure you tell us in writing and on what the hotels, trains and airlines we booked will refund to us. We pass on every refund we receive, minus the charges set out below, within [14] working days of receiving it.",
    "sections": [
        ("How to cancel", [
            "Write to us at the email address on your booking confirmation. Your cancellation takes effect on the day we receive it. A message on WhatsApp is welcome, but please follow it with an email so we have a written record.",
            "If more than one person is booked and only some cancel, we recalculate the price for those still travelling, since rooms and cars are priced per party.",
        ]),
        ("Our cancellation scale", [
            "These charges are a percentage of the total journey price and apply unless a supplier's own terms are stricter (see the next section).",
            {"list": [
                "[61] days or more before departure: we keep the deposit of [25]%.",
                "[60–31] days before departure: [50]% of the total price.",
                "[30–15] days before departure: [75]% of the total price.",
                "[14] days or fewer, or no-show: [100]% of the total price.",
            ]},
        ]),
        ("Supplier terms that may be stricter", [
            "Some services carry their own non-refundable terms, which we tell you about in your quote before you book. Common examples are peak-season hotel stays (Durga Puja, Diwali, Christmas, New Year and the May school holidays), toy train tickets, protected-area permits for Nathu La, Tsomgo and North Sikkim once issued, Dooars safari tickets, Bhutan's Sustainable Development Fee once the permit is processed, and flights on non-refundable fares. Where a supplier refunds nothing, we cannot refund that part.",
        ]),
        ("If we have to change or cancel", [
            "If we cancel your journey for any reason other than events outside our control, we refund everything you have paid us in full.",
            "If a significant part of the journey changes before departure (for example a different hotel in a lower category), we offer you a comparable alternative, a price adjustment, or a full refund of the affected part.",
        ]),
        ("Events outside anyone's control", [
            "Landslides on NH10 and the North Sikkim roads, snow closures at Nathu La and Zero Point, flash floods, forest closures in the Dooars, strikes, government restrictions and similar events can change a route. We will reroute you as close to the original plan as we can and pass on any refund or credit suppliers give us. We recommend travel insurance that covers cancellation for these reasons.",
        ]),
        ("Refunds", [
            "Refunds go back to the account you paid from, in Indian rupees, within [14] working days of us receiving the money back from suppliers. Bank and card charges and currency differences are not refundable. [Confirm whether payment gateway fees are refunded.]",
        ]),
        ("Changes instead of cancellation", [
            "Moving your dates is often cheaper than cancelling. Changes requested more than [45] days before departure carry no fee from us; suppliers may charge for theirs. We confirm every change in writing.",
        ]),
    ],
}

POLICIES["booking-terms"] = {
    "title": "Booking terms and conditions",
    "nav": "Booking terms",
    "summary": "Prices on this site are indicative. Your written quote is the offer; a booking is confirmed when we receive your deposit and send written confirmation. Travel insurance with medical evacuation cover is a condition of booking.",
    "sections": [
        ("Who we are", [
            "Go Sikkim Tours is a trading name of [LEGAL NAME], registered at [REGISTERED ADDRESS], [COMPANY REGISTRATION NO.], GSTIN [GSTIN], [MINISTRY OF TOURISM APPROVAL NO. IF HELD].",
        ]),
        ("Prices and quotes", [
            "Prices on the website are indicative 'from' prices in Indian rupees, per person, twin sharing, for the tier shown (Budget, Value or Comfort). They are not offers. Your written quote lists the services, hotels, room categories, dates and total price, including applicable GST. A quote is valid for [7] days unless it says otherwise, and remains subject to availability until booked.",
        ]),
        ("Booking and payment", [
            "To book, accept the quote in writing and pay the deposit of [25]% of the total price. We then confirm every service in writing. The balance is due [45] days before departure; bookings made within [45] days are paid in full. See the payments policy for methods.",
        ]),
        ("Your responsibilities", [
            "You must hold a valid passport and visa where required, the permits we tell you about for restricted areas, and travel insurance that covers medical evacuation and, for North Sikkim, Nathu La, Sandakphu, Goecha La and Bhutan's passes, altitudes up to the highest point on your route. Please tell us about health conditions, mobility needs and diets when you book.",
        ]),
        ("Our responsibilities", [
            "We plan and book your journey with care and use suppliers we have worked with. Hotels, airlines, railways, parks and other suppliers provide their services under their own terms. Where something goes wrong on the ground, tell your planner straight away so we can help while you are still there.",
        ]),
        ("Changes, cancellations and refunds", [
            "See our refund and cancellation policy, which forms part of these terms.",
        ]),
        ("Complaints", [
            "If something is not right, tell your planner during the journey. If it is not resolved, write to [COMPLAINTS EMAIL] within [30] days of your return and we will reply within [14] days.",
        ]),
        ("Law", [
            "These terms are governed by the laws of India. Courts in [CITY] have jurisdiction.",
        ]),
    ],
}

POLICIES["payments"] = {
    "title": "Payments policy",
    "nav": "Payments",
    "summary": "We take a [25]% deposit to confirm a booking and the balance [45] days before departure. You can pay by [UPI, bank transfer (NEFT/RTGS/IMPS, SWIFT for overseas) or card]. We never ask for card details by email, WhatsApp or phone.",
    "sections": [
        ("When you pay", [
            {"list": [
                "Deposit: [25]% of the total price, to confirm your booking.",
                "Balance: due [45] days before departure.",
                "Late bookings (within [45] days of departure): full payment at booking.",
                "Some suppliers (Bhutan permits and the SDF, toy train seats, festival-period hotels) need early payment; your quote will say so.",
            ]},
        ]),
        ("How you can pay", [
            "[Confirm accepted methods.] Indian residents: UPI, NEFT/RTGS/IMPS bank transfer, credit and debit cards through [PAYMENT GATEWAY]. Overseas clients: SWIFT transfer in INR or [USD/EUR/GBP], or international cards through [PAYMENT GATEWAY]. Card payments may carry a gateway fee of [X]%, shown before you pay.",
        ]),
        ("Taxes", [
            "Prices in quotes include GST at the applicable rate, shown separately on your invoice. Tax Collected at Source (TCS) may apply to some packages under Indian tax law; we show it on the invoice where it does. [Confirm with your accountant.]",
        ]),
        ("Keeping payments safe", [
            "Our bank details are only ever sent on a signed PDF invoice from [ACCOUNTS EMAIL]. If you receive bank details from any other address, or a message asking you to pay a different account, call us on [PHONE] before paying. We never ask for card numbers, OTPs or passwords.",
        ]),
    ],
}

POLICIES["privacy"] = {
    "title": "Privacy policy",
    "nav": "Privacy",
    "summary": "We collect the details you give us to plan and book your journey, and use them for nothing else. We share only what a hotel, airline, permit office or guide needs to provide a booked service. We do not sell your data.",
    "sections": [
        ("What we collect", [
            "When you enquire: your name, email, phone number and the details of the journey you describe. When you book: passport details and dates of birth where hotels, permits or airlines require them, dietary and health notes you choose to share, and payment records. When you subscribe to our letter: your email address.",
        ]),
        ("How we use it", [
            "To reply to your enquiry, plan and book your journey, look after you while you travel, keep accounting records and, if you subscribed, send our monthly letter. We do not use your data for advertising profiles.",
        ]),
        ("Who we share it with", [
            "Only the suppliers who provide a service you booked (hotels, airlines, railways, parks and permit offices, drivers and guides) and our accountants and payment providers. Some are outside India; we share only what each one needs.",
        ]),
        ("How long we keep it", [
            "Enquiries that do not lead to a booking: [24] months. Booking records: as long as Indian tax and accounting law requires, currently [8] years. Newsletter: until you unsubscribe.",
        ]),
        ("Your rights", [
            "You can ask to see, correct or delete your personal data, or withdraw consent for our letter, by writing to [PRIVACY EMAIL]. We reply within [30] days. Under India's Digital Personal Data Protection Act you may also contact our grievance officer: [NAME, EMAIL].",
        ]),
        ("This website", [
            "The site sets a security cookie for its forms and no advertising cookies. It loads fonts from Google Fonts, scripts from cdnjs and unpkg, and photographs from Wikimedia, and those services see your IP address when your browser requests their files. Our maps are drawn on our own server, with no map service. See the cookie policy for details.",
        ]),
    ],
}

POLICIES["cookies"] = {
    "title": "Cookie policy",
    "nav": "Cookies",
    "summary": "This website uses one essential cookie to protect its forms. It uses no advertising or tracking cookies unless we add analytics, in which case this page will list them.",
    "sections": [
        ("Essential", [
            "csrftoken: set by our website software to protect forms from cross-site attacks. Expires after one year. Contains no personal data.",
        ]),
        ("Stored in your browser", [
            "If you close the small planning prompt on guide pages, your browser remembers that for the rest of the visit (session storage) so we do not show it again. Nothing is sent to us.",
        ]),
        ("Analytics", [
            "[If you enable Google Analytics 4, list its cookies here (_ga, _ga_*) and add a consent banner before setting them.]",
        ]),
    ],
}

POLICIES["disclaimer"] = {
    "title": "Disclaimer",
    "nav": "Disclaimer",
    "summary": "We work hard to keep the information on this site accurate, but permits, park seasons, road and pass openings, festival dates, timings and prices change, sometimes at short notice. Check current status before you travel; your written quote is what counts.",
    "sections": [
        ("Information on this site", [
            "Our guides, journeys and place pages describe conditions as we understand them when written. They are for planning, not a guarantee. Distances and drive times are typical, not exact. Prices are indicative.",
        ]),
        ("Health and altitude", [
            "Our notes on altitude, heat and health are general advice, not medical advice. Please see a doctor before travelling, especially to North Sikkim (Gurudongmar is about 5,430 m), Nathu La, Sandakphu, Goecha La or Bhutan's high passes.",
        ]),
        ("Photographs", [
            "Photographs come from Wikimedia Commons under free licences and are credited to their authors. They show places as they were when photographed. See our photo credits page.",
        ]),
        ("Maps", [
            "Our maps are drawn from Natural Earth outlines (public domain), with international borders as depicted by India. They show where places are, and are not for navigation.",
        ]),
        ("Links", [
            "Links to hotels and other sites are for convenience. We are not responsible for their content.",
        ]),
    ],
}

POLICIES["accessibility"] = {
    "title": "Accessibility statement",
    "nav": "Accessibility",
    "summary": "We want this site to work for everyone, including people who use screen readers, keyboards or zoom. We aim for WCAG 2.2 level AA. If something does not work for you, tell us and we will fix it or give you the information another way.",
    "sections": [
        ("What we have done", [
            {"list": [
                "Text contrast of at least 4.5:1, with each land's colours tested.",
                "Every page works with a keyboard, with visible focus outlines.",
                "Photos have text alternatives; maps have a numbered list of every place shown.",
                "Animations stop if your device asks for reduced motion.",
                "The site works without JavaScript, apart from the trip tools.",
            ]},
        ]),
        ("Travelling with access needs", [
            "Many heritage sites have steps and uneven ground. Tell us about mobility, sight, hearing or other needs and we will check hotels, vehicles and sites for you before you book.",
        ]),
        ("Contact", [
            "Write to [ACCESSIBILITY EMAIL] or call [PHONE].",
        ]),
    ],
}
