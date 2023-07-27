/*var el = document.getElementById('occ').value;
console.log(el)*/
select = document.getElementById('spec');
console.log(select);
const occ = document.getElementById('occ');

function removeOptions(selectElement) {
    var i, L = selectElement.options.length - 1;
    for(i = L; i >= 0; i--) {
        selectElement.remove(i);
    }
}

occ.addEventListener('change', function handleChange(event) {


// using the function:
console.log(occ.options[occ.selectedIndex].value);
var el = occ.options[occ.selectedIndex].value;


if (el != ''){
    removeOptions(document.getElementById('spec'));
}

if( el == "doctors"){
    theArray = ['All','Accident and emergency','Anaesthesia','Cardiology','Dermatology','Diabetes','Ear Nose and Throat', 'Gastroenterology', 'General Practitioner', 'Haematology',
    'Histopathology','Infectious Disease', 'Intensive Care', 'MAU', 'Medicine', 'Microbiology','Neonates','Nephrology','Neurology','Obstetrics','Oncology','Opthalmology',
    'Otolaryngology','Orthopaedics','Paediatrics','Pathology','Psychiatry','Radiology','Surgery','Urology']
    for (const element of theArray) {
    var opt = document.createElement('option');
    opt.value = element;
    opt.innerHTML = element;
    select.appendChild(opt);
    }
}

else if( el == "nursing"){
    theArray = ['All','Accident and emergency','Adults','Children','Community','Intensive Care','Learning Disabilities','Mental Health','Neonatal', 'Prison','General nurse','Theatre']
    for (const element of theArray) {
    var opt = document.createElement('option');
    opt.value = element;
    opt.innerHTML = element;
    select.appendChild(opt);
    }
}

else if( el == "dental"){
    theArray = ['All','Orthodontics','Surgery','Periodontics','Prosthodontics','Endodontics']
    for (const element of theArray) {
    var opt = document.createElement('option');
    opt.value = element;
    opt.innerHTML = element;
    select.appendChild(opt);
    }
}

else if( el == "midwifery"){
    theArray = ['All']
    for (const element of theArray) {
    var opt = document.createElement('option');
    opt.value = element;
    opt.innerHTML = element;
    select.appendChild(opt);
    }
}

else if( el == "social_care"){
    theArray = ['All']
    for (const element of theArray) {
    var opt = document.createElement('option');
    opt.value = element;
    opt.innerHTML = element;
    select.appendChild(opt);
    }
}

else if( el == "ahp"){
    theArray = ['All','Audiology','Biomedical science','Clinical assesor', 'Dietitan','Medical lab','Occupational therapy','Orthoptics','Paramedics','Physiotherapy','Podiatrist','Prosthetist',
    'Radiography','Sonography','Logotherapy','Speech therapy']
    for (const element of theArray) {
    var opt = document.createElement('option');
    opt.value = element;
    opt.innerHTML = element;
    select.appendChild(opt);
    }
}
});
