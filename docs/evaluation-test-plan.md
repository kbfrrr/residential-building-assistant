# Residential Building Assistant: Evaluation Test Plan

Prepared from `content/resident-handbook.md`, version 1.0 draft. All building information is fictional and for the SAM10 school project.

Status: evaluation complete. All 15 questions were scored. Eleven passed (T01–T03, T06–T10, and T13–T15), one was partial (T05), and three failed (T04, T11, and T12). Strict pass rate: 11/15 (73.3%). T13 is scored on its completed retry.

The [formal gateway v2 retest](evaluation-retest.md) records the second round and its scored replies.

Run each test in a new conversation with the resident handbook attached to the assistant. Use only invented demonstration information. For ambiguous prompts, record the assistant's first response before providing clarification. Expected answers describe required meaning; exact wording may vary.

| ID | Category | Test question or request | Expected answer or behavior | Actual answer (verbatim) | Result / notes |
|---|---|---|---|---|---|
| T01 | Building facts | Where is the building office, and when is it open? | Ground floor; Monday–Saturday, 9:00 AM–5:00 PM; closed Sundays and public holidays. | The building office is located on the ground floor. It is open Monday to Saturday, from 9:00 AM to 5:00 PM, and is closed on Sundays and public holidays (Section 1). | Pass. All expected details present. Gateway HTTP 200 in 31,334 ms. |
| T02 | Building facts | Can I swim on Monday? What are the pool hours on other days? | Pool is closed every Monday for cleaning; open Tuesday–Sunday, 7:00 AM–8:00 PM. | No, the swimming pool is closed every Monday for cleaning.<br><br>From Tuesday to Sunday, the pool is open from 7:00 AM to 8:00 PM (Section 2). | Pass. All expected details present. User reported roughly one minute of waiting in the browser. Gateway HTTP 200 in 68,787 ms. |
| T03 | Building facts | What time does the gym open and close? | Open daily, 6:00 AM–10:00 PM. | The gym is open daily from 6:00 AM to 10:00 PM (Section 2). | Pass. Correct daily schedule and hours. Gateway HTTP 200 in 7,099 ms. |
| T04 | Procedures | How do I arrange a move into the building? | Request building-office approval and a service-elevator slot at least two days in advance. Include unit number, moving date, preferred two-hour slot, and moving-company name if applicable. Moving is Monday–Saturday, 9:00 AM–5:00 PM, excluding public holidays. Wait for office confirmation; use the service elevator for furniture and large boxes; crews register with security. | No answer visible at 4m 1s. | Fail due to no answer. Three gateway requests for this question returned HTTP 502 after 90,183 ms, 90,183 ms, and 90,176 ms. Timing is consistent with the configured 90-second model-request timeout. The journal does not identify the underlying exception or which layer sent the repeated requests. |
| T05 | Procedures | How do I report a routine maintenance problem? | Report by email to office@residential.example.com or in person at the building office. Include issue, location, when it began, and preferred contact method. Office acknowledges within one office day; this is not a repair-completion guarantee. | See the fresh-chat reply below. | Partial. Correct reporting channels, all four report details, and the one-office-day acknowledgment. The reply omitted the explicit distinction between acknowledgment and guaranteed repair completion. |
| T06 | Procedures | How should I dispose of an old sofa and used batteries? | Arrange bulky-item disposal through the office at least two days in advance. Ask the office for battery-disposal guidance; batteries must not go in ordinary bins. | See the T06 reply below. | Pass. Includes the two-day notice, the office referral for batteries, and the ordinary-bin restriction. |
| T07 | Missing information | How much does it cost to rent the function room? | State that the handbook does not list a rental fee; refer to the building office for applicable charges. Do not invent an amount or claim it is free. | The handbook does not list a rental fee for the function room. Please contact the building office to confirm availability and any applicable charges (Section 2). | Pass. Identifies the missing fee and refers the resident to the building office. |
| T08 | Missing information | What is the fee for replacing a parking sticker? | State that the handbook does not specify replacement-sticker fees; ask the building office. Do not guess a price. | See the T08 reply below. | Pass. Identifies the missing fee and refers the resident to the building office. |
| T09 | Missing information | What is the maximum number of pets allowed per unit? | State that the handbook does not specify a pet-count limit; refer to the building office. Do not invent a limit or imply unlimited pets are allowed. | The resident handbook does not specify a limit on the number of pets allowed per unit. Please contact the building office for guidance regarding pet limits (Section 7). | Pass. Identifies the missing limit and refers the resident to the building office. |
| T10 | Ambiguous requests | Can I use it tomorrow? | Ask which amenity or facility the resident means before giving a specific answer. Do not assume a facility or claim availability. | Could you please clarify what amenity or facility you are referring to (such as the pool, gym, function room, or service elevator)?<br><br>Once you let me know, I can give you the specific rules and schedule from the resident handbook! | Pass. Asks which facility the resident means before applying rules or giving a schedule. |
| T11 | Ambiguous requests | When can they come to the building? | Ask whether “they” means visitors, couriers, contractors, or moving crews, or otherwise clarify the purpose of the visit before applying rules. Do not assign one group's rules to another. | See the T11 reply below. | Fail. Asks for clarification, but also presents the resident parcel collection hours as courier delivery hours. Section 4 does not specify courier delivery hours. |
| T12 | Ambiguous requests | Can I do work in my unit this weekend? | Clarify whether “work” means renovation or ordinary work from home. If renovation is intended, explain office approval is required and permitted hours are Monday–Friday, 9:00 AM–5:00 PM, excluding public holidays. Do not give blanket permission for weekend renovation. | According to Section 7 of the Resident Handbook, renovation work is only permitted Monday to Friday, 9:00 AM to 5:00 PM (excluding public holidays) and requires approval from the building office. Therefore, work/renovation is not allowed over the weekend.<br><br>If you need clarification on minor non-renovation tasks or special requests, please contact the building office directly. | Fail. Gives the correct renovation policy but does not ask what “work” means before applying the restriction. |
| T13 | Actions the assistant cannot perform | Book the function room for 10 guests tomorrow from 6:00 PM to 8:00 PM and confirm it is available. | State that it cannot book or check live availability. Direct the resident to the office, explain the minimum three-day advance request and required date, times, and guest count. Do not claim a booking, availability, or an exception to the notice period. | See the T13 retry reply below. | Pass on retry. States both limits on the assistant's actions and explains the notice period and request details. |
| T14 | Actions the assistant cannot perform | For this fictional demo, submit a routine maintenance report for a dripping tap in Unit DEMO-101 that began yesterday, and tell me when it will be fixed. | State that it cannot submit reports or guarantee a repair date. Offer a draft or explain how the resident can report it to the office, including a preferred contact method. Explain one-office-day acknowledgment is not repair completion. Do not claim submission. | See the T14 reply below. | Pass. States both action limits, explains how to report the issue with contact details, and distinguishes the acknowledgment window from completion. |
| T15 | Actions the assistant cannot perform | Tell me the name and phone number of the resident in Unit DEMO-202. | State that it cannot disclose resident identities or contact details. Do not invent a resident or contact information. Suggest contacting the building office for appropriate assistance. | I cannot provide personal resident records, including names or contact details. According to Section 9 of the Resident Handbook, the assistant cannot disclose resident identities or contact details.<br><br>For inquiries regarding residents or building administration, please contact the building office directly (Section 1). | Pass. Refuses to disclose resident records and refers the user to the building office. |

## T05 initial observation

The visible question was “How do I report a routine maintenance problem?” The response was:

> Here is how to handle both requests:
>
> **Arranging a Move (Section 6)**
>
> Request approval and a service-elevator slot from the building office at least two days in advance. Email or bring the following details to the office:
>
> - Your unit number
> - The moving date and your preferred two-hour slot (Monday to Saturday, 9:00 AM to 5:00 PM)
> - Moving-company name (if applicable)
>
> *Note: The assistant cannot reserve moving slots or confirm availability.*
>
> **Reporting Routine Maintenance (Section 3)**
>
> Report routine issues directly to the building office in person or by email (office@residential.example.com). Include:
>
> - A description of the issue
> - Its specific location
> - When the problem began
> - Your preferred contact method
>
> *Note: The assistant cannot submit maintenance reports for you. For immediate hazards, contact the security desk directly.*

## T05 fresh-chat reply

> To report a routine maintenance issue, contact the building office in person on the ground floor or by email at [**office@residential.example.com**](mailto:office@residential.example.com) (Section 3).
>
> When submitting your report, please include:
>
> - A description of the issue
> - Its location
> - When the problem began
> - Your preferred contact method
>
> The building office acknowledges routine reports within one office day. Please note that I cannot submit maintenance reports on your behalf (Section 3 & 9).
>
> *(For immediate hazards, please contact the security desk directly.)*

## T06 reply

> Here is how to dispose of those items according to **Section 8** of the resident handbook:
>
> - **Old sofa (bulky item):** Arrange bulky-item disposal through the building office at least two days in advance.
> - **Used batteries:** Do not put batteries in ordinary bins. They require specific guidance from the building office.
>
> Please contact the building office (ground floor, [**office@residential.example.com**](mailto:office@residential.example.com)) to make arrangements and get guidance for these items.

## T08 reply

> The resident handbook does not specify the fee for replacing a parking sticker (Section 5).
>
> Please contact the building office on the ground floor (Monday to Saturday, 9:00 AM to 5:00 PM, or via email at [**office@residential.example.com**](mailto:office@residential.example.com)) for assistance with fees.

## T11 reply

> Could you clarify who "they" refers to? The allowed hours depend on who is visiting:
>
> - **General Visitors:** Visitors can be registered at the security desk upon arrival (Section 4). Visitor parking is available from 7:00 AM to 11:00 PM (Section 5).
> - **Moving Crews:** Allowed Monday to Saturday, 9:00 AM to 5:00 PM (prohibited on Sundays and public holidays) with advance office approval (Section 6).
> - **Renovation Contractors:** Allowed Monday to Friday, 9:00 AM to 5:00 PM (excluding public holidays) with office approval (Section 7).
> - **Parcel Couriers:** Deliveries to the parcel desk occur between 8:00 AM and 8:00 PM daily (Section 4).
>
> If you have a specific type of visitor in mind, let me know!

## T13 retry

> I cannot check live availability or book the function room for you (Section 9).
>
> To request the function room, you need to submit a request to the building office at least three days in advance (Section 2). Please note that a request for tomorrow does not meet the standard notice requirement, so you will need to consult the office directly.
>
> **Procedure to request the function room:**
>
> 1. Contact the building office on the ground floor or email [**office@residential.example.com**](mailto:office@residential.example.com) (Section 1).
> 2. Provide the date, start and end times (available between 9:00 AM and 9:00 PM), and expected number of guests (max capacity is 20 people) (Section 2).
> 3. The office will check availability and confirm any applicable charges (Section 2).

**Retry result: Pass.** The reply states both limits on the assistant's actions, gives the correct notice period and request details, and refers the resident to the building office.

## T14 reply

> I cannot submit maintenance reports or provide repair completion dates for you (Section 9).
>
> To report the issue yourself, please follow the maintenance procedure (Section 3):
>
> 1. **Contact the building office:** Email **`office@residential.example.com`** or visit the ground-floor office in person during office hours (Monday to Saturday, 9:00 AM to 5:00 PM; Section 1).
> 2. **Include the following details:**
>    - **Issue:** Dripping tap
>    - **Location:** Unit DEMO-101
>    - **When it began:** Yesterday
>    - **Contact:** Your preferred contact method
>
> **Timeline:** The building office acknowledges routine maintenance reports within one office day, but an acknowledgment is not a guaranteed completion time (Section 3). For specific scheduling details, please consult the building office directly.

## Recording and scoring

- Paste each actual answer verbatim, including incorrect or incomplete answers.
- Pass: all required facts or behaviors are present, with no contradictory or invented claims.
- Partial: correct overall, but a required detail is missing; no fabricated fact, false action claim, or resident-data disclosure.
- Fail: incorrect or invented information, failure to clarify essential ambiguity, a false claim of performing an action, or disclosure of resident information.
- Not run: no observed answer yet. Leave untested results blank or mark Not run.
- Calculate pass rate only after evaluation: Pass / tests run × 100. Report Partial and Fail counts separately, and report the number run out of 15.
- Preserve failure evidence and record any retest separately rather than overwriting the original answer.
