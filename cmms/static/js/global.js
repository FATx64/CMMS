function parseJSON(response) {
    return response.text().then((text) => {
        return JSONbig.parse(text)
    })
}

