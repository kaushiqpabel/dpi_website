const searchOpen = document.getElementById('searchOpen');
const mobileModeSearchForm = document.getElementById('mobile-mode-search-form');
const searchBack = document.getElementById('searchBack');

const regKeyToggle = document.getElementById('reg-key-toggle');
const regKeyDropdown = document.getElementById('reg-key-dropdown');
const userToggle = document.getElementById('user-toggle');
const userDropdown = document.getElementById('user-dropdown');

const bloodGroupData = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];
const genderData = ["Male", "Female"];
const jobTypeData = ['Government', 'Private', 'Bussiness', 'Homemaker', 'Others'];
const searchCriteria = ["Gender", "Blood Group", "Job Type", "Department"];
const contactAndSocialMediaData = ["Phone Number", "WhatsApp", "Viber", "Telegram", "Signal", "Imo", "Facebook", "Instagram", "LinkedIn", "TikTok", "YouTube", "X(Twitter)", "GitHub"];

const departmentData = ['Civil Eng.', "Architectural Eng.", "Environmental Eng.", "Mechanical Eng.", "Chemical Eng.", "Food Eng.", "Electrical Eng.", "Electronics Eng.", "Computer Eng.", "Power Eng.", "Automobile Eng.", "RAC Eng."];

if(regKeyToggle){
  regKeyToggle.addEventListener("click", function() {
    if(regKeyDropdown.style.display == 'block'){
      regKeyDropdown.style.display = 'none';
    }else {
      regKeyDropdown.style.display = 'block';
    }
  });

}


if(userToggle){
  userToggle.addEventListener('click', function(){
    if(userDropdown.style.display == 'block'){
      userDropdown.style.display = 'none';
    }else {
      userDropdown.style.display = 'block';
    }
  });
}

document.addEventListener('click', function(e) {
  if(regKeyToggle){
    if(e.target !== regKeyToggle && !regKeyToggle.contains(e.target)){
      regKeyDropdown.style.display = 'none';
    }
  }


  if(userToggle){
    if(e.target !== userToggle && !userToggle.contains(e.target)){
      userDropdown.style.display = 'none';
    }
  }


});



if(searchOpen){
  searchOpen.addEventListener('click', () => {
    mobileModeSearchForm.classList.add('active');
  });
}

if(searchBack){
  searchBack.addEventListener('click', () => {
    mobileModeSearchForm.classList.remove('active');
  });
}

const desktopModeSearchCriteriaInputElement = document.getElementById("desktop-mode-search-criteria-input");
if(desktopModeSearchCriteriaInputElement){
  const searchDropdown = document.getElementById("search-criteria-dropdown");
  const searchValueInputContainer = document.getElementById("desktop-mode-search-value-input-container");
  desktopModeSearchCriteriaInputElement.addEventListener("focus", function(){
    createDropdown(this, searchDropdown, searchCriteria,  null, searchValueInputContainer);    
  });
  hideDropdown(searchDropdown, ".search-input-container");
}

const mobileModeSearchCriteriaInputElement = document.getElementById("mobile-mode-search-criteria-input");
if(mobileModeSearchCriteriaInputElement){
  const searchDropdown = document.getElementById("mobile-mode-search-dropdown");
  const searchValueInputContainer = document.getElementById("mobile-mode-search-value-input-container");
  mobileModeSearchCriteriaInputElement.addEventListener("focus", function(){
    createDropdown(this, searchDropdown, searchCriteria,  null, searchValueInputContainer);  
  });
  hideDropdown(searchDropdown, ".search-input-container");
}

function createSearchData(searchType, searchValueInputContainer){
  let optionsData = null;
  if(searchType === "Blood Group"){
    optionsData = bloodGroupData;
  }else if (searchType === "Gender"){
    optionsData = genderData;
  }else if (searchType === "Department"){
    optionsData = departmentData;
  }else {
    optionsData = jobTypeData;
  }
  searchValueInputContainer.innerHTML = `
      <div class="search-input-container">
          <input autocomplete="off" readonly name="search-value" placeholder="Select One" class="input-field" id="search-value-input"/>
          <span class="selection-dropdown-arrow">▼</span>
          <div id="search-value-dropdown"></div>
      </div>
  `;
  searchValueInputContainer.style.width = "100%";
  const searchValueInput = document.getElementById("search-value-input");
  const dropdown = document.getElementById("search-value-dropdown");
  searchValueInput.addEventListener("focus", function(){
      createDropdown(this, dropdown, optionsData);
  });
  hideDropdown(dropdown, '.search-input-container');
}

const desktopModeSearchForm = document.getElementById("desktop-mode-search-form");
if(desktopModeSearchForm){
    desktopModeSearchForm.addEventListener("submit", function (e) {   
        const desktopModeSearchCriteriaInputValue = desktopModeSearchCriteriaInputElement.value.trim();
        if(!desktopModeSearchCriteriaInputValue){
          e.preventDefault();
          showMessageBox(desktopModeSearchCriteriaInputValue, "Select Search Criteria", "Please select a search criteria to proceed.");
          return;
        }
        const searchValueInputElement = document.getElementById("search-value-input");
        if(searchValueInputElement){
          const searchValue = searchValueInputElement.value.trim();
          if(!searchValue){
            e.preventDefault();
            showMessageBox(searchValueInputElement, "Select Search Item", "Please select a search item to proceed.");
            return;
          }
        }
    });
}


if(mobileModeSearchForm){
    mobileModeSearchForm.addEventListener("submit", function (e) {   
        const mobileModeSearchCriteriaInputValue = mobileModeSearchCriteriaInputElement.value.trim();
        if(!mobileModeSearchCriteriaInputValue){
          e.preventDefault();
          showMessageBox(mobileModeSearchCriteriaInputValue, "Select Search Criteria", "Please select a search criteria to proceed.");
          return;
        }
        const searchValueInputElement = document.getElementById("search-value-input");
        if(searchValueInputElement){
          const searchValue = searchValueInputElement.value.trim();
          if(!searchValue){
            e.preventDefault();
            showMessageBox(searchValueInputElement, "Select Search Item", "Please select a search item to proceed.");
            return;
          }
        }
    });
}


const downloadRegKeyLink = document.getElementById("download-reg-key");
if(downloadRegKeyLink){
  downloadRegKeyLink.addEventListener("click", (e) => {
      e.preventDefault();
      const cellElements = document.getElementsByClassName("cell");
      let textContent = "Available Registration Keys \n";
      for(let i = 0; i < cellElements.length; i++){
        const cellElement = cellElements[i];
        textContent += `${i+1}) ${cellElement.textContent} \n`;
      }
      const blob = new Blob([textContent], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'registration_keys.txt';
      link.click();
      URL.revokeObjectURL(url);
  });
}

// Date of birth script
function renderCalendar(date) {
  const year = date.getFullYear();
  const month = date.getMonth();
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const monthNames = ["January","February","March","April","May","June","July","August","September","October","November","December"];
  
  // Dropdown for month and year
  let html = `
    <div class="calendar-header">
      <select id="monthSelect" onchange="jumpToMonthYear()">
        ${monthNames.map((m, i) => `<option value="${i}" ${i===month?"selected":""}>${m}</option>`).join("")}
      </select>
      <select id="yearSelect" onchange="jumpToMonthYear()">
        ${getYearOptions(year)}
      </select>
    </div>
    <table>
      <thead>
        <tr><th>Su</th><th>Mo</th><th>Tu</th><th>We</th><th>Th</th><th>Fr</th><th>Sa</th></tr>
      </thead>
      <tbody>
        <tr>
  `;

  for (let i = 0; i < firstDay; i++) {
    html += "<td></td>";
  }

  for (let day = 1; day <= daysInMonth; day++) {
    const dayOfWeek = (firstDay + day - 1) % 7;
    html += `<td onclick="selectDate(${year}, ${month}, ${day})">${day}</td>`;
    if (dayOfWeek === 6 && day < daysInMonth) {
      html += "</tr><tr>";
    }
  }
  html += "</tr></tbody></table>";
  calendar.innerHTML = html;
}

function getYearOptions(currentYear) {
  let options = "";
  for (let y = currentYear - 100; y <= currentYear + 20; y++) {
    options += `<option value="${y}" ${y===currentYear?"selected":""}>${y}</option>`;
  }
  return options;
}

function jumpToMonthYear() {
  const month = parseInt(document.getElementById("monthSelect").value);
  const year = parseInt(document.getElementById("yearSelect").value);
  currentDate = new Date(year, month, 1);
  renderCalendar(currentDate);
}

function selectDate(year, month, day) {
  const m = String(month + 1).padStart(2, "0");
  const d = String(day).padStart(2, "0");
  dateOfBirthElement.value = `${year}-${m}-${d}`;
  calendar.style.display = "none";
}

function changeMonth(offset) {
  currentDate.setMonth(currentDate.getMonth() + offset);
  renderCalendar(currentDate);
}

const dateOfBirthElement = document.getElementById("date-of-birth"); 
if(dateOfBirthElement){
  const calendar = document.getElementById("calendar");
  let currentDate = new Date();

  dateOfBirthElement.addEventListener("focus", () => {
    calendar.style.display = "block";
    renderCalendar(currentDate);
  });

  document.addEventListener("click", (e) => {
    if (!calendar.contains(e.target) && e.target !== dateOfBirthElement) {
      calendar.style.display = "none";
    }
  });
}

const SOCIAL_PATTERNS = {
  Facebook: /^(?:https?:\/\/)?(?:www\.)?facebook\.com\/[A-Za-z0-9\.]+\/?$/,
  Instagram: /^(?:https?:\/\/)?(?:www\.)?instagram\.com\/[A-Za-z0-9_\.]+\/?$/,
  TikTok: /^(?:https?:\/\/)?(?:www\.)?tiktok\.com\/@?[A-Za-z0-9_.]+\/?$/,
  YouTube: /^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(channel\/|c\/|@|user\/)?[A-Za-z0-9_\-]+|youtu\.be\/[A-Za-z0-9_\-]+)/,
  LinkedIn: /^(?:https?:\/\/)?(?:[a-z]{2,3}\.)?linkedin\.com\/(in|company)\/[A-Za-z0-9_\-]+\/?$/,
  GitHub: /^(?:https?:\/\/)?(?:www\.)?github\.com\/[A-Za-z0-9_\-]+\/?$/,
  "X(Twitter)": /^(?:https?:\/\/)?(?:www\.)?(?:twitter\.com|x\.com)\/[A-Za-z0-9_]+\/?$/,
};

// Contact 
const contactListInput = document.getElementById("contact-list-input");
if(contactListInput){
   const contactDropdown = document.getElementById("contact-dropdown"); 
   const contactInputContainer = document.getElementById("contact-input-container");
   contactListInput.addEventListener("focus", function () {
      const currentContactListInputs = document.getElementsByName("contact_type[]");
      let allContact = contactAndSocialMediaData;
      if(currentContactListInputs){
        currentContactListInputs.forEach(contactInput => {
            let index = allContact.indexOf(contactInput.value);
            if(index !== -1){
              allContact.splice(index, 1);
            }
        });
      }
      if(allContact.length){
        createDropdown(this, contactDropdown, allContact, addItemToContactInputContainer);
        return
      }
      contactListInput.blur();
   });

   hideDropdown(contactDropdown, ".contact-selection-field");

   contactInputContainer.addEventListener("focusin", function(e){
      const element = e.target;
      if(element.classList.contains("contact-value-input")){
          element.parentElement.style.borderColor = "#0047AB";
      }
   });

   contactInputContainer.addEventListener("focusout", function(e){
      const element = e.target;
      if(element.classList.contains("number-based-contact")){
          element.parentElement.style.borderColor = "#ccc";
          const fullRegex = /^\+?[0-9\s().-]{6,20}$/;
          if (element.value && !fullRegex.test(element.value)) {
            showMessageBox(element, "Invalid Format", `<b>"${element.value}"</b> is not a valid phone number. Please enter a valid phone number.`);
            element.value = "";
          }
      }else if(element.classList.contains("link-based-contact")){
          element.parentElement.style.borderColor = "#ccc";
          const userText = element.dataset.platform;
          let currentString = element.value.trim();
          if(currentString){
            const PATTERN = SOCIAL_PATTERNS[userText];
            if (!/^https?:\/\//.test(currentString)) {
              currentString = "https://" + currentString; // add https:// if missing
            }
            if(!PATTERN.test(currentString)){
              showMessageBox(element, "Invalid link", `"${currentString}" is not a valid <b>${userText}</b> link. Please enter a valid <b>${userText}</b> link.`);
              element.value = "";
            }
          }
      }
   });

   contactInputContainer.addEventListener("input", function(e){
        const element = e.target;
        if(element.classList.contains("number-based-contact")){
          element.value = element.value.replace(/[^0-9+\s\-().]/g, '');
        }
   });

   contactInputContainer.addEventListener("click", function(e){
        const element = e.target;
        if(element.classList.contains("remove-contact")){
          element.parentElement.parentElement.remove(); 
        }else if(element.classList.contains("remove-contact-path")){
          element.parentElement.parentElement.parentElement.remove();
        }
   });
}


function addItemToContactInputContainer(userText){
  const number_based_contact = ['Phone Number', 'WhatsApp', 'Viber', 'Telegram', 'Signal', 'Imo'];
  const contactInputContainer = document.getElementById("contact-input-container");
  let contactInputBoxWrapperContainer = document.createElement("div");
  contactInputBoxWrapperContainer.innerHTML = `
  <label class="contact-label" for="contact-input-${userText}">${userText}</label>
  <div class="contact-input-box">
      <input type="hidden" name="contact_type[]" value="${userText}"/>
      ${(() => {
        if(number_based_contact.includes(userText)){
          return `<input autocomplete="off" type="text" class="number-based-contact contact-value-input" name="contact_value[]" id="contact-input-${userText}" placeholder="${getPlaceholderText(userText)}"/>`;
        }else {
          return `<input autocomplete="off" type="text" data-platform="${userText}" class="link-based-contact contact-value-input" name="contact_value[]" id="contact-input-${userText}" placeholder="${getPlaceholderText(userText)}"/>`
        }
      })()}
      ${createSVG()}
  </div>`;
  contactInputContainer.appendChild(contactInputBoxWrapperContainer);
  document.getElementById(`contact-input-${userText}`).focus();
}

function getPlaceholderText(userText){
  const number_based_app = ['WhatsApp', 'Viber', 'Telegram', 'Signal', "Imo"];
  if(userText === "Phone Number"){
    return `Enter your ${userText}`;
  }else if(number_based_app.includes(userText)){
    return `Enter your ${userText} number`;
  }else if(userText === 'YouTube'){
    return `Paste your ${userText} channel link`;
  }else {
    return `Paste your ${userText} account link`;
  }
}

function createSVG() {
  return  (`
    <svg class="remove-contact" style="width: 1.5em; height: 1.5em;vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <title>remove contact</title>
    <path class="remove-contact-path" d="M810.65984 170.65984q18.3296 0 30.49472 12.16512t12.16512 30.49472q0 18.00192-12.32896 30.33088l-268.67712 268.32896 268.67712 268.32896q12.32896 12.32896 12.32896 30.33088 0 18.3296-12.16512 30.49472t-30.49472 12.16512q-18.00192 0-30.33088-12.32896l-268.32896-268.67712-268.32896 268.67712q-12.32896 12.32896-30.33088 12.32896-18.3296 0-30.49472-12.16512t-12.16512-30.49472q0-18.00192 12.32896-30.33088l268.67712-268.32896-268.67712-268.32896q-12.32896-12.32896-12.32896-30.33088 0-18.3296 12.16512-30.49472t30.49472-12.16512q18.00192 0 30.33088 12.32896l268.32896 268.67712 268.32896-268.67712q12.32896-12.32896 30.33088-12.32896z"  /></svg> 
  `);  
}

// Message Box Scripts
let elementToFocus = null;
const messageBoxContainer = document.getElementById('message-box-container');
const messageBoxHeaderBodyContainer = document.getElementById("message-box-header-body-container");
const messsageBoxCloseButton = document.getElementById("message-box-close-button");

messsageBoxCloseButton.addEventListener('click', () => {
  messageBoxContainer.style.display = "none";
  if(elementToFocus && document.body.contains(elementToFocus)){
    setTimeout(() => elementToFocus.focus(), 10);
  }
});

if(messageBoxHeaderBodyContainer.innerHTML.trim() !== ""){
  messageBoxContainer.style.display = "block";
}

function showMessageBox(sourceElement, msgTitle, msgBody){
  messageBoxContainer.style.display = "block";
  messageBoxHeaderBodyContainer.innerHTML = `
      <h2>${msgTitle}</h2>
      <div class="card-content">${msgBody}</div>`;
  elementToFocus = sourceElement || null;
}

function validateFile(input, allowedExtensions, allowedTypes) {
    const file = input.files[0];
    if (!file) return null; // no file selected, let backend handle required check
    const fileName = file.name.toLowerCase();
    const fileType = file.type; // MIME type from browser (not 100% reliable)
    const extValid = allowedExtensions.some(ext => fileName.endsWith(ext));
    const typeValid = allowedTypes.includes(fileType);
    if (!extValid || !typeValid) {
        input.value = ""; // reset file input
        return null;
    }
    return file;
}

const genderListInput = document.getElementById("gender-list-input");
if(genderListInput){
  const genderDropdown = document.getElementById("gender-dropdown");
  genderListInput.addEventListener("focus", function() {
      createDropdown(this, genderDropdown, genderData);
  });
  hideDropdown(genderDropdown, ".gender-selection-field");
}


const departmentListInput = document.getElementById("department-list-input");
if(departmentListInput){
  const departmentDropdown = document.getElementById("department-dropdown");
  departmentListInput.addEventListener("focus", function() {
      createDropdown(this, departmentDropdown, departmentData);
  });
  hideDropdown(departmentDropdown, ".department-selection-field");
}


function createDropdown(listInput, dropdownContainer, listItems, callbackFunc=null, searchValueInputContainer=null){
  dropdownContainer.innerHTML = "";
  const dropdown = document.createElement("div");
  const corner = document.createElement("div");
  dropdown.classList.add("selection-list-container");
  corner.classList.add("selection-dropdown-corner");
  
  listItems.forEach(item => {
      const option = document.createElement("div");
      option.textContent = item;
      option.onclick = () => {
        if (callbackFunc){
          callbackFunc(item);
        }else {
          listInput.value = item;
        }
        dropdownContainer.innerHTML = "";
        if(searchValueInputContainer){
            createSearchData(item, searchValueInputContainer);
        }
      };
      dropdown.appendChild(option);   
  });
  dropdownContainer.appendChild(corner);
  dropdownContainer.appendChild(dropdown);
  if(searchValueInputContainer){
      searchValueInputContainer.innerHTML = "";
      searchValueInputContainer.style.width = "0px";
  }
}

function hideDropdown(dropdownContainer, selectionField){
  document.addEventListener("click", (e) => {
    if (!e.target.closest(selectionField)) {
      if(dropdownContainer){
        dropdownContainer.innerHTML = "";
      }
    }
  });
}

const bloodGroupListInput = document.getElementById("blood-group-list-input");
if(bloodGroupListInput){
  const bloodGroupDropdown = document.getElementById("blood-group-dropdown");
  bloodGroupListInput.addEventListener("focus", function() {
      createDropdown(this, bloodGroupDropdown, bloodGroupData);
  });
  hideDropdown(bloodGroupDropdown, ".blood-group-selection-field");
}

const jobTypeListInput = document.getElementById("job-type-list-input");
if(jobTypeListInput){
  const jobTypeDropdown = document.getElementById("job-type-dropdown");
  jobTypeListInput.addEventListener("focus", function() {
      createDropdown(this, jobTypeDropdown, jobTypeData);
  });
  hideDropdown(jobTypeDropdown, ".job-type-selection-field");
}

const userForm = document.getElementById("user-form");
if(userForm){
  userForm.addEventListener("submit", function (e) {   
      const fullNameElement = document.getElementById("full-name");
      const fullNameValue = fullNameElement.value.trim();
      if(!fullNameValue){
        e.preventDefault();
        showMessageBox(fullNameElement, "Add Full Name", "Full name field cannot be empty.");
        return;
      }
      const bioElement = document.getElementById("profile-bio");
      const bioValue = bioElement.value.trim();
      if(!bioValue){
        e.preventDefault();
        showMessageBox(bioElement, "Add Bio", "Bio field cannot be empty.");
        return;
      }
      console.log(dateOfBirthElement.value);
      const dateOfBirthValue = dateOfBirthElement.value.trim();
      if(!dateOfBirthValue){
        e.preventDefault();
        showMessageBox(dateOfBirthElement, "Add Date of Birth", "Date of birth field cannot be empty.");
        return;
      }

      const genderElement = document.getElementById("gender-list-input");
      const genderValue = genderElement.value.trim();
      if(!genderValue){
        e.preventDefault();
        showMessageBox(genderElement, "Add Gender", "Gender field cannot be empty.");
        return;
      }

      const bloodGroupElement = document.getElementById("blood-group-list-input");
      const bloodGroupValue = bloodGroupElement.value.trim();
      if(!bloodGroupValue){
        e.preventDefault();
        showMessageBox(bloodGroupElement, "Add Blood Group", "Blood Group field cannot be empty.");
        return;
      }

      const departmentElement = document.getElementById("department-list-input");
      const departmentValue = departmentElement.value.trim();
      if(!departmentValue){
        e.preventDefault();
        showMessageBox(departmentElement, "Add Department", "Department field cannot be empty.");
        return;
      }

  });
}

const profilePhotoInputElement = document.getElementById('profile-photo-upload-input');
if(profilePhotoInputElement){
  const facelessIconElement = document.getElementById("faceless-icon-element");
  const noProfilePhotoButton = document.getElementById("no-profile-photo-button");
  const profilePhotoStatusInput = document.getElementById("profile-photo-status-input");
  const profilePhotoResetButton = document.getElementById("profile-photo-reset-button");
  const profilePhotoPeviewElement = document.getElementById('profile-photo-preview-element');
  const savedProfilePhotoElement = document.getElementById('saved-profile-photo-element');
  let uploadedProfilePhotoFile = null;
  
  facelessIconElement.style.display = 'none';
  profilePhotoPeviewElement.style.display = 'none';

  profilePhotoInputElement.addEventListener('change', function() {
    uploadedProfilePhotoFile = validateFile(this, [".jpg", ".jpeg", ".png"], ["image/jpeg", "image/png"]);
    if(uploadedProfilePhotoFile){
      profilePhotoPeviewElement.src = URL.createObjectURL(uploadedProfilePhotoFile);
      profilePhotoPeviewElement.style.display = 'block';
      savedProfilePhotoElement.style.display = 'none';
      facelessIconElement.style.display = 'none';
      profilePhotoStatusInput.value = "changed";
    }else{
      showMessageBox(this, "Invalid file type.", "The selected file is not supported by the system. Please upload a file with .jpg, .jpeg or .png extension.");
    }    
  });

  profilePhotoResetButton.addEventListener('click', function() {
      profilePhotoInputElement.value = "";
      profilePhotoPeviewElement.style.display = 'none';
      savedProfilePhotoElement.style.display = 'block';
      facelessIconElement.style.display = 'none';
      profilePhotoStatusInput.value = "unchanged";
  });
  noProfilePhotoButton.addEventListener("click", function(){
    facelessIconElement.style.display = 'block';
    profilePhotoPeviewElement.style.display = 'none';
    savedProfilePhotoElement.style.display = 'none';
    profilePhotoStatusInput.value = "initial";
    profilePhotoInputElement.value = "";
  });
}


const resumeInputElement = document.getElementById('resume-upload-input');
if(resumeInputElement){
  const blankResumeElement = document.getElementById('blank-resume-element');
  const noResumeButton = document.getElementById("no-resume-button");
  const resumeStatusInput = document.getElementById("resume-status-input");
  const resumeResetButton = document.getElementById("resume-reset-button");
  const resumePeviewElement = document.getElementById('resume-preview-element');
  const savedResumeElement = document.getElementById('saved-resume-element');
  let uploadedResumeFile = null;
  
  blankResumeElement.style.display = 'none';
  resumePeviewElement.style.display = 'none';

  resumeInputElement.addEventListener('change', function() {
    uploadedResumeFile = validateFile(this, [".jpg", ".jpeg", ".png", ".pdf"], ["image/jpeg", "image/png", "application/pdf"]);
    if(uploadedResumeFile){
      resumePeviewElement.href = URL.createObjectURL(uploadedResumeFile);
      resumePeviewElement.style.display = 'block';
      savedResumeElement.style.display = 'none';
      blankResumeElement.style.display = 'none';
      resumeStatusInput.value = "changed";
    }else {
      showMessageBox(this, "Invalid file type.", "The selected file is not supported by the system. Please upload a file with .jpg, .jpeg, .png or .pdf extension.");
    }    
  });

  resumeResetButton.addEventListener('click', function() {
      resumeInputElement.value = "";
      resumePeviewElement.style.display = 'none';
      blankResumeElement.style.display = 'none';
      savedResumeElement.style.display = 'block';
      resumeStatusInput.value = "unchanged";
  });

  noResumeButton.addEventListener("click", function(){
    resumeStatusInput.value = "initial";
    blankResumeElement.style.display = 'block';
    resumePeviewElement.style.display = 'none';
    savedResumeElement.style.display = 'none';
    resumeInputElement.value = "";
  });
}


const timerDisplay = document.getElementById('otp-timer');
if(timerDisplay){  
    const timeLeftInput = document.getElementById('time-left-input');
    const submitResendOtpButton = document.getElementById("submit-resend-otp-button");

    let timeLeft = parseInt(timeLeftInput.value);

    function updateTimer() {
      // Calculate minutes and seconds
      const minutes = Math.floor(timeLeft / 60);
      const seconds = timeLeft % 60;

      // Format as MM:SS
      timerDisplay.textContent = 
        `${String(minutes).padStart(2,'0')}:${String(seconds).padStart(2,'0')}`;

      // Stop timer when time is up
      if (timeLeft <= 0) {
        document.getElementById('otp').disabled = true;
        document.getElementById("otp-time-container").innerHTML =  `
            <div class="password-criteria red-border-background text-align-center">
                <p>OTP is no longer valid.</p>
            </div>`;
        submitResendOtpButton.textContent = 'Send Again'
        return;
      }
      timeLeft--;
    }
    setInterval(updateTimer, 1000);
    updateTimer();
}
		
		 