var addReviewButton = document.getElementById("addReviewButton");

var addReviewDiv = document.getElementById("addReviewDiv");
var nameElement = document.getElementById("name");
var ratingElement = document.getElementById("rating");
var reviewElement = document.getElementById("review");
var submitReviewButton = document.getElementById("submitReviewButton");
var cancelButton = document.getElementById("cancelButton");

var resetReviewDiv = function() {
    nameElement.value = "";
    ratingElement.value = "10";
    reviewElement.value = "";
};

var addReview = function() {
    addReviewDiv.hidden = false;
    addReviewButton.disabled = true;
    resetReviewDiv();
};

var cancelReview = function() {
    addReviewDiv.hidden = true;
    addReviewButton.disabled = false;
    resetReviewDiv();
};

var disableButtons = function() {
    cancelButton.disabled = true;
    submitReviewButton.disabled = true;
};

var enableButtons = function() {
    cancelButton.disabled = false;
    submitReviewButton.disabled = false;
};

var submitReview = function() {
    var data = {};

    if (!nameElement.value) {
        data.name = "Anonymous";
    }
    else {
        if (nameElement.value.length > 40) {
            return Swal.fire("Name too long", "40 characters max allowed", "error");
        }
        data.name = nameElement.value;
    }

    if (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"].includes(ratingElement.value)) {
        data.rating = parseInt(ratingElement.value);
    }
    else {
        return Swal.fire("Please rate the place on the scale of 1 to 10.", "", "error");
    }

    if (!reviewElement.value) {
        return Swal.fire("Please type your review.", "", "error");
    }
    else {
        if (reviewElement.value.length > 10000) {
            return Swal.fire("Review too long", "10000 characters max allowed", "error");
        }
        data.review = reviewElement.value;
    }

    disableButtons();

    var xhttp = new XMLHttpRequest();
    xhttp.onerror = function() {
        enableButtons();
        return Swal.fire("An unknown error occurred!", "Please try again.", "error");
    };
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            enableButtons();

            if (this.status == 200) {
                var response = JSON.parse(this.responseText);
                console.log(response);
                if (response.success) {
                    cancelReview();
                    Swal.fire("Your review has been published successfully!", "", "success");
                    window.setTimeout(function() {window.location.reload();}, 2000);
                    return;
                }
                return Swal.fire("An unknown error occurred!", "Please try again.", "error");
            }
            return Swal.fire("An unknown error occurred!", "Please try again.", "error");
        }
    };
    xhttp.open("POST", window.location.href, true);
    xhttp.send(JSON.stringify(data));
};

addReviewButton.addEventListener("click", addReview);
submitReviewButton.addEventListener("click", submitReview);
cancelButton.addEventListener("click", cancelReview);
