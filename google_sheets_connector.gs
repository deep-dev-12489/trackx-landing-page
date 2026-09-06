/**
 * TrackX.ai — Google Sheets Live Offer Connector
 * 
 * This script connects your TrackX.ai Landing Page directly to a Google Sheet!
 * Every offer submitted on your website will automatically create a new row in your Google Sheet.
 * 
 * INSTRUCTIONS:
 * 1. Open Google Sheets (https://sheets.new) and create a blank spreadsheet named "TrackX.ai Offers".
 * 2. Click "Extensions" > "Apps Script".
 * 3. Paste this entire code into the script editor.
 * 4. Click "Deploy" (top right) > "New deployment".
 * 5. Select type: "Web app".
 * 6. Set "Execute as": Me
 * 7. Set "Who has access": Anyone (Crucial for receiving offers from your website!)
 * 8. Click "Deploy", copy the "Web app URL", and paste it into index.html (GOOGLE_WEB_APP_URL)!
 */

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Create header row if empty
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        "Timestamp", 
        "Full Name", 
        "Email Address", 
        "Phone Number", 
        "Country", 
        "Preferred Channel", 
        "Channel ID / Handle", 
        "Offer Amount (USD)", 
        "Intended Use"
      ]);
      sheet.getRange("A1:I1").setFontWeight("bold").setBackground("#0f172a").setFontColor("#ffffff");
    }

    var data;
    if (e.postData && e.postData.contents) {
      data = JSON.parse(e.postData.contents);
    } else {
      data = e.parameter;
    }

    // Append response row
    sheet.appendRow([
      new Date(),
      data.full_name || "",
      data.email || "",
      data.phone || "",
      data.country || "",
      data.channel || "",
      data.channel_handle || "",
      data.offer_amount || "",
      data.intended_use || ""
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ "result": "success", "message": "Offer recorded in Google Sheet!" }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ "result": "error", "error": error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput("TrackX.ai Google Sheet Webhook is Live!");
}
