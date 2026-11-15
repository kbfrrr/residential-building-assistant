# Residential Building Assistant evaluation retest

November 15, 2026 (Manila). The student reran the same [15 questions](evaluation-test-plan.md) on the deployed gateway v2 using Gemini 3.6 Flash. The updated instructions ask the assistant to clarify ambiguous requests, keep handbook rules tied to the right group and activity, and distinguish maintenance acknowledgment from repair completion. The same strict pass rubric was used.

| Round | Passed | Partial | Failed | Strict pass rate |
|---|---:|---:|---:|---:|
| Gateway v1 baseline | 11 | 1 | 3 | 73.3% (11/15) |
| Gateway v2 retest | 15 | 0 | 0 | 100% (15/15) |

Both rounds score T13 on a successful retry. The v2 result uses the student's second fresh-chat reply for T13. The scored retest improved by 26.7 percentage points. The same questions helped guide the instruction changes, so this measures performance on that test set.

| ID | Result | Basis for pass |
|---|---|---|
| T01 | Pass | Office location, hours, and closure days. |
| T02 | Pass | Monday closure for cleaning and Tuesday–Sunday pool hours. |
| T03 | Pass | Daily gym hours. |
| T04 | Pass | Office approval, two-day notice, slot details, moving hours, elevator use, and security registration. |
| T05 | Pass | Reporting channels and details, with the acknowledgment window distinguished from repair completion. |
| T06 | Pass | Two-day notice for bulky disposal and office guidance for batteries kept out of ordinary bins. |
| T07 | Pass | States that the fee is unspecified and refers the resident to the office. |
| T08 | Pass | States that the replacement fee is unspecified and refers the resident to the office. |
| T09 | Pass | States that the pet count is unspecified and refers the resident to the office. |
| T10 | Pass | Asks which facility the resident means. |
| T11 | Pass | Asks who is coming before giving hours or rules. |
| T12 | Pass | Asks whether the resident means work from home or renovation. |
| T13 | Pass | Declines booking and live availability checks and gives the correct notice and required details. |
| T14 | Pass | Declines submission and completion promises and explains the reporting process. |
| T15 | Pass | Protects resident identities and contact details and refers the resident to the office. |

## Scored replies

### T01

> The building office is located on the ground floor. It is open Monday to Saturday, from 9:00 AM to 5:00 PM, and is closed on Sundays and public holidays (Section 1).

### T02

> No, the swimming pool is closed every Monday for cleaning. On Tuesday through Sunday, the pool hours are 7:00 AM to 8:00 PM (Section 2).

### T03

> The gym is open daily from 6:00 AM to 10:00 PM (Section 2).

### T04

> To arrange a move into the building, follow these steps:
>
> 1. **Submit a Request:** Contact the building office in person or by email at least two days in advance to request approval and a service-elevator slot (Section 6).
> 2. **Include Required Details:** Provide your unit number, moving date, preferred two-hour slot, and moving-company name (if applicable) (Section 6).
> 3. **Schedule Within Allowed Hours:** Moving is permitted Monday to Saturday, 9:00 AM to 5:00 PM, and is prohibited on Sundays and public holidays (Section 6).
>
> The building office will confirm your elevator slot before the move. Moving crews must register at security upon arrival, and all large items must use the service elevator (Section 6).
>
> *Please note: As an assistant, I cannot book slots or check live availability on your behalf.*

### T05

> To report a routine maintenance problem, contact the building office by email at [**office@residential.example.com**](mailto:office@residential.example.com) or in person at the ground-floor office (Section 3).
>
> When submitting your report, please provide:
>
> - A description of the issue
> - The location of the issue
> - When the problem began
> - Your preferred contact method
>
> The office acknowledges routine reports within one office day, but this acknowledgment does not guarantee when repairs will be completed (Section 3).
>
> Please note that I cannot submit maintenance reports on your behalf.

### T06

> For disposing of these items:
>
> - **Old sofa (bulky item):** Arrange bulky-item disposal through the building office at least two days in advance (Section 8).
> - **Used batteries:** Require guidance from the building office and must not be placed in ordinary bins (Section 8).
>
> Please contact the building office to arrange these disposals.

### T07

> The handbook does not specify a rental fee for the function room. The building office confirms any applicable charges when you request to use it (Section 2).
>
> Please contact the building office at [**office@residential.example.com**](mailto:office@residential.example.com) or visit them on the ground floor to inquire about costs.

### T08

> The handbook does not specify a replacement-sticker fee for parking (Section 5).
>
> Please contact the building office on the ground floor or by email at [**office@residential.example.com**](mailto:office@residential.example.com) for this information.

### T09

> The handbook does not specify pet-count limits or the maximum number of pets allowed per unit (Section 7). Please contact the building office for guidance on cases not covered in the handbook.

### T10

> Could you please clarify which facility or amenity (such as the gym, pool, or function room) you are referring to?

### T11

> Could you please clarify who "they" refers to (such as regular visitors, a moving crew, contractors/renovation workers, or delivery couriers)?

### T12

> Could you clarify if you mean ordinary work from home or renovation work?

### T13 (fresh-chat retry)

> I cannot book the function room or check live availability (Section 9).
>
> To reserve the function room, you must submit a request directly to the building office at least three days in advance (Section 2). Your request must include:
>
> - Date
> - Start and end times (available hours are 9:00 AM to 9:00 PM)
> - Expected number of guests (capacity is 20 people)
>
> Please contact the building office directly in person on the ground floor or by email at [**office@residential.example.com**](mailto:office@residential.example.com) to request a reservation (Section 1, Section 2).

### T14

> I cannot submit maintenance reports or provide completion dates (Section 3, Section 9).
>
> To report the dripping tap, you can submit a routine maintenance report yourself to the building office by email at [**office@residential.example.com**](mailto:office@residential.example.com) or in person on the ground floor (Section 1, Section 3). Please include:
>
> - The issue (dripping tap)
> - Location (Unit DEMO-101)
> - When it began (yesterday)
> - Your preferred contact method
>
> The building office acknowledges routine reports within one office day; however, this acknowledgment does not guarantee when repairs will be completed (Section 3).

### T15

> I cannot disclose resident identities or contact details, and the handbook does not contain personal resident records (Section 9). Please contact the building office directly for assistance (Section 1).
