var inputs = document.querySelectorAll('input');
var inputDetails = [];

inputs.forEach(function (input) {
    var label = document.querySelector(`label[for='${input.id}']`) || input.closest('label');
    var labelText = label ? label.innerText.trim() : '';
    if (labelText) {
        inputDetails.push({ label: labelText, element: input });
    }
});

return inputDetails;
