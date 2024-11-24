

function validateToken(token) {
    return new Promise((resolve, reject) => {
        fetch("https://www.haxball.com/rs/api/host", {
            headers: {
                accept: "",
                "accept-language": "tr,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                "content-type": "application/x-www-form-urlencoded",
                "sec-ch-ua":
                  '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                Referer: "https://html5.haxball.com/",
                "Referrer-Policy": "strict-origin-when-cross-origin",
            },
            body: `token=${token}&rcr=`,
            method: "POST",
        }).then(async (response) => {
            response = await response.json();
            if(response.data == null)
                reject("An error occured with API.")
            
            switch(response.data.action) {
                case "connect":
                    resolve("Valid token")
                    break;

                case "recaptcha":
                    reject("Token is invalid.")
                    break;
            }
        }).catch((e) => reject(e))
    })
}

window.onHBLoaded = () => {
    validateToken("{{token}}").then((msg) => console.log(msg)).catch((e) => console.log(e.toString()))
}
