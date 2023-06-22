const favoriteIcons = document.querySelectorAll(".favorite-icon");
const csrfToken = document.querySelector('#csrf-token input[name="csrfmiddlewaretoken"]').value;


favoriteIcons.forEach(favoriteIcon =>
    favoriteIcon.addEventListener("click", () => {
        const companyId = favoriteIcon.getAttribute("data-company-id");
        const request = new XMLHttpRequest();
        const formData = new FormData()
        formData.append("company_id", companyId);
        let url = "/manage-favorites/";

        request.open('POST', url);
        request.setRequestHeader("X-CSRFToken", csrfToken);
        request.send(formData);

        request.onload = function () {
            if (request.status === 200){
                const response = JSON.parse(request.responseText);

                if (is_authenticated){
                    if (response["is_favorite"]){
                        favoriteIcon.textContent = "bookmark_border";
                    } else {
                        favoriteIcon.textContent = "bookmark";
                    }
                } else {

                }
            } else {
                console.log(request.status)
            }
        };
    })
);
