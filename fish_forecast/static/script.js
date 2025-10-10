//JavaScript to handle form submission and fetch coordinates
// Using OpenCage Geocoding API
// code below created by co-pilot

      document.getElementById("locationForm").addEventListener("submit", function(e) {
        e.preventDefault();
        const location = document.getElementById("location").value;

        const apiKey = "1a01d4aa2eec4f97a8a60af24e3802ce";
        const url = `https://api.opencagedata.com/geocode/v1/json?q=${encodeURIComponent(location)}&key=${apiKey}&countrycode=us&limit=1`;

        fetch(url)
          .then(response => response.json())
          .then(data => {
            if (data.results.length > 0) {
              const lat = data.results[0].geometry.lat;
              const lng = data.results[0].geometry.lng;
          
              document.getElementById("output").innerText = `Location: Latitude: ${lat}, Longitude: ${lng}`;

              // Send to Flask backend
              fetch("/save_settings", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json"
                },
                body: JSON.stringify({ lat: lat, lng: lng})
              })
              .then(response => response.json())
              .then(data => {
                console.log("Coordinates saved:", data);
              })
              .catch(error => {
                console.error("Error sending coordinates:", error);
              });

            } else {
              document.getElementById("output").innerText = "Location not found.";
            }
          })
          .catch(error => {
            console.error("Error fetching coordinates:", error);
            document.getElementById("output").innerText = "Error fetching coordinates.";
          });
      });
