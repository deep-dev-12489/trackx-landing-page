/**
 * TrackX.ai — Google Form Automated Generator
 * 
 * INSTRUCTIONS:
 * 1. Go to https://script.google.com/
 * 2. Click "New project"
 * 3. Paste this entire code into Editor (Code.gs)
 * 4. Click "Save" (Ctrl+S or Cmd+S) and then click "Run" at the top
 * 5. Review permissions when prompted
 * 6. View the Execution Log at the bottom to get your Form Share Link and Embed Code!
 */

function createTrackXOfferForm() {
  // Create a new Google Form
  var form = FormApp.create('TrackX.ai — Make an Offer');
  
  // Set form description & confirmation message
  form.setDescription('Submit your offer for the acquisition of the premium domain name TrackX.ai.');
  form.setConfirmationMessage("Thanks — I'll reach out on your preferred channel within 24 hours.");
  
  // Field 1: Full Name (Short Answer, Required)
  form.addTextItem()
      .setTitle('Full Name')
      .setRequired(true);

  // Field 2: Email Address (Short Answer, Required, Email Validation)
  var emailItem = form.addTextItem()
      .setTitle('Email Address')
      .setRequired(true);
  var emailValidation = FormApp.createTextValidation()
      .requireTextIsEmail()
      .setHelpText('Please enter a valid email address.')
      .build();
  emailItem.setValidation(emailValidation);

  // Field 3: Phone Number (Short Answer, Required)
  form.addTextItem()
      .setTitle('Phone Number')
      .setRequired(true);

  // Field 4: Country (Short Answer, Required)
  form.addTextItem()
      .setTitle('Country')
      .setRequired(true);

  // Field 5: Preferred messaging channel (Multiple Choice, Required)
  form.addMultipleChoiceItem()
      .setTitle('Preferred messaging channel')
      .setChoiceValues(['WhatsApp', 'Telegram', 'Signal', 'WeChat', 'iMessage', 'Other'])
      .setRequired(true);

  // Field 6: Your ID/handle on that channel (Short Answer, Required with Helper Text)
  form.addTextItem()
      .setTitle('Your ID/handle on that channel')
      .setHelpText('e.g. your WhatsApp number, Telegram @username, etc.')
      .setRequired(true);

  // Field 7: Your offer amount (USD) (Short Answer, Required, Number Validation)
  var offerItem = form.addTextItem()
      .setTitle('Your offer amount (USD)')
      .setRequired(true);
  var offerValidation = FormApp.createTextValidation()
      .requireNumberGreaterThan(0)
      .setHelpText('Please enter a valid numeric offer amount in USD.')
      .build();
  offerItem.setValidation(offerValidation);

  // Field 8: Intended use for the domain (Paragraph, Optional)
  form.addParagraphTextItem()
      .setTitle('Intended use for the domain')
      .setRequired(false);

  // Retrieve Links & Embed Details
  var publishedUrl = form.getPublishedUrl();
  var editUrl = form.getEditUrl();
  var embedCode = '<iframe src="' + publishedUrl + '?embedded=true" width="100%" height="950" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>';

  Logger.log('====================================================');
  Logger.log('🎉 GOOGLE FORM CREATED SUCCESSFULLY!');
  Logger.log('====================================================');
  Logger.log('Shareable Form Link: ' + publishedUrl);
  Logger.log('Form Edit Link: ' + editUrl);
  Logger.log('Embed HTML Code:\n' + embedCode);
  Logger.log('====================================================');
}
