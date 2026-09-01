/*
 GST COMPLIANCE DATA — EDIT THIS FILE ONLY FOR DUE-DATE CHANGES.
 Keep this file in the same folder as compliance.html.

 OVERRIDE EXAMPLE:
 GST_COMPLIANCE_OVERRIDES["2026-09-11"] = {
   date: "2026-09-13",
   status: "Extended by Notification",
   note: "Due date extended to 13 Sep 2026."
 };

 IMPORTANT:
 - Base rules are normal statutory/planning dates.
 - Extensions/special notifications should be entered in OVERRIDES.
 - If a rule changes permanently, edit the relevant RULES entry.
*/
window.GST_COMPLIANCE_OVERRIDES = {
  /* "2026-09-11": {date:"2026-09-13", status:"Extended by Notification", note:"Government extension"} */
};

window.GST_COMPLIANCE_RULES = [
  {name:"GSTR-1", day:11, profile:"regular", type:"return", review:"Outward supplies, amendments, credit/debit notes and HSN/SAC.", months:[0,1,2,3,4,5,6,7,8,9,10,11]},
  {name:"GSTR-1 – QRMP quarterly", day:13, profile:"qrmp", type:"return", review:"Quarterly outward-supply statement.", quarterEndOnly:true, months:[2,5,8,11]},
  {name:"GSTR-6", day:13, profile:"isd", type:"return", review:"Input Service Distributor return.", months:[0,1,2,3,4,5,6,7,8,9,10,11]},
  {name:"GSTR-5", day:13, profile:"special", type:"return", review:"Non-resident taxable person return; verify current applicability.", months:[0,1,2,3,4,5,6,7,8,9,10,11]},
  {name:"GSTR-7", day:10, profile:"tds", type:"return", review:"GST TDS return and deducted-tax details.", months:[0,1,2,3,4,5,6,7,8,9,10,11]},
  {name:"GSTR-8", day:10, profile:"tcs", type:"return", review:"GST TCS statement for e-commerce operators.", months:[0,1,2,3,4,5,6,7,8,9,10,11]},
  {name:"GSTR-3B", day:20, profile:"regular", type:"return", review:"Summary liability, ITC, reversals, interest/late fee and payment.", months:[0,1,2,3,4,5,6,7,8,9,10,11]},
  {name:"GSTR-3B – QRMP Group 1", day:22, profile:"qrmp", type:"return", review:"Quarterly GSTR-3B for notified Group 1 States/UTs.", quarterEndOnly:true, months:[2,5,8,11]},
  {name:"GSTR-3B – QRMP Group 2", day:24, profile:"qrmp", type:"return", review:"Quarterly GSTR-3B for notified Group 2 States/UTs.", quarterEndOnly:true, months:[2,5,8,11]},
  {name:"QRMP PMT-06", day:25, profile:"qrmp", type:"payment", review:"Monthly tax payment for M1/M2 of the quarter, where applicable.", quarterFirstTwoOnly:true, months:[0,1,3,4,6,7,9,10]},
  {name:"CMP-08", day:18, profile:"composition", type:"payment", review:"Quarterly statement-cum-challan for composition taxpayers.", quarterEndOnly:true, months:[2,5,8,11]}
];

window.GST_ANNUAL_RULES = [
  {name:"GSTR-9 / GSTR-9C – Annual compliance", month:11, day:31, profile:"regular", type:"annual", review:"Annual return / reconciliation statement where applicable. Confirm turnover threshold and latest notified due date."},
  {name:"GSTR-4 Annual – Composition", month:3, day:30, profile:"composition", type:"annual", review:"Annual return for composition taxpayers; confirm latest notified due date."},
  {name:"ITC-04 – Annual cycle", month:3, day:25, profile:"special", type:"annual", review:"Job-work movement reporting where annual frequency applies; verify turnover/frequency conditions."},
  {name:"ITC-04 – Half-yearly cycle", month:8, day:25, profile:"special", type:"annual", review:"Job-work movement reporting where half-yearly frequency applies; verify applicability."}
];
