//JavaScript to handle form submission and fetch coordinates
// Code below created with assistance of co-pilot

// Variable to store the selected fish
let fish_species = null;

// Get all dropdown options
const fishOptions = document.querySelectorAll('#fish_species .dropdown-option');


// Add click event listener to each option
fishOptions.forEach(option => {
  option.addEventListener('click', () => {
    fish_species = option.getAttribute('data-value');
    console.log('Selected fish:', fish_species);
    
    // Optional: Add visual feedback for selection
    fishOptions.forEach(opt => opt.classList.remove('selected'));
    option.classList.add('selected');

    const imagepath = `/static/images/${fish_species}.png`;
    const chosen_fish = fish_species.charAt(0).toUpperCase() + fish_species.slice(1);
    console.log('Image path:', imagepath);
    console.log('Chosen fish:', chosen_fish);
    const observer = new MutationObserver(() => {
      const imageElement = document.getElementById('selectedFishImage');
      const nameElement = document.getElementById('selectedFishName');

      if (imageElement && nameElement) {
        imageElement.src = imagepath;
        imageElement.alt = chosen_fish;
        nameElement.textContent = chosen_fish;
        observer.disconnect(); // Stop observing once done
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
    });
});



document.getElementById("locationForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const location = document.getElementById("location").value;
  console.log("Location submitted:", location);
      
  // Send to Flask backend
  fetch("/location_change", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ location: location, fish_species: fish_species })
  })
  
  .then(response => response.json())
  
  .then(weather_data => {
    console.log("weather forecasted:", weather_data);
    document.getElementById("result").innerHTML = `                 
      <!-- weather forecast card -->
  
      <div class="card" style="width: 18rem;">
      ...
      <div class="card-body">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-cloud h-8 w-8 text-gray-500" aria-hidden="true"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"></path>
        </svg>
      <h5 class="card-title">Current Weather</h5>
      </div>   
                
      <ul class="list-group list-group-flush"> 
        <li class="list-group list-group-flush">  
          <p>Location: ${weather_data.region}, ${weather_data.country}</p>                  
          <p>Date/Time: ${weather_data.localtime}</p>
        </li>                 
        <li class="list-group-item">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-thermometer h-4 w-4" aria-hidden="true"><path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z">
            </path>
          </svg>${weather_data.avgtemp_f}°F</li>
        </li>
        <li class="list-group-item">
          Condition: ${weather_data.condition}</li>
        <li class="list-group-item">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-wind h-4 w-4" aria-hidden="true"><path d="M12.8 19.6A2 2 0 1 0 14 16H2"></path><path d="M17.5 8a2.5 2.5 0 1 1 2 4H2"></path><path d="M9.8 4.4A2 2 0 1 1 11 8H2"></path></svg>
          <p>Wind Speed (mph): ${weather_data.wind_mph}</p>    
          <p>Max Wind (mph): ${weather_data.maxwind_mph}</p>
        </li>
        <li class="list-group-item">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-droplets h-4 w-4" aria-hidden="true"><path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"></path><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"></path></svg>
          Humidity: ${weather_data.humidity}
        </li>
        <li class="list-group-item">Pressure (in): ${weather_data.pressure_in}</li>
                                      
      </ul>
      </div>  
      <!-- Moon Phase card -->
      <div class="card" style="width: 18rem;">
      ...
      <div class="card-body">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-moon h-8 w-8 text-yellow-500" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z"></path></svg>
        <h5 class="card-title">Current Moon Phase</h5>
      </div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">Phase Name: ${weather_data.moon_phase}</li>
        <li class="list-group-item">Moon Rise: ${weather_data.moonrise}</li>
        <li class="list-group-item">Moon Set: ${weather_data.moonset} </li>
      </ul>
      <div class="card-body">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sun h-8 w-8 text-yellow-500" aria-hidden="true">
        <circle cx="12" cy="12" r="4"></circle>
        <path d="M12 2v2"></path>
        <path d="M12 20v2"></path>
        <path d="M5.22 5.22l1.42 1.42"></path>
        <path d="M17.36 17.36l1.42 1.42"></path>
        <path d="M2 12h2"></path>
        <path d="M20 12h2"></path>
        <path d="M5.22 18.78l1.42-1.42"></path>
        <path d="M17.36 6.64l1.42-1.42"></path>             
      </svg>              
      <h5 class="card-title">Current Sun Phase</h5>
      </div>
      <ul class="list-group list-group-flush">                      
        <li class="list-group-item">Sunrise: ${weather_data.sunrise}</li>
        <li class="list-group-item">Sunset: ${weather_data.sunset} </li>
      </ul>
      </div>
      <!-- Fish Forecast Card -->
      <div class="card" style="width: 18rem;">
      ...
      <div class="card-body">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-fish h-8 w-8 text-blue-600" aria-hidden="true"><path d="M6.5 12c.94-3.46 4.94-6 8.5-6 3.56 0 6.06 2.54 7 6-.94 3.47-3.44 6-7 6s-7.56-2.53-8.5-6Z"></path><path d="M18 12v.5"></path><path d="M16 17.93a9.77 9.77 0 0 1 0-11.86"></path><path d="M7 10.67C7 8 5.58 5.97 2.73 5.5c-1 1.5-1 5 .23 6.5-1.24 1.5-1.24 5-.23 6.5C5.58 18.03 7 16 7 13.33"></path><path d="M10.46 7.26C10.2 5.88 9.17 4.24 8 3h5.8a2 2 0 0 1 1.98 1.67l.23 1.4"></path><path d="m16.01 17.93-.23 1.4A2 2 0 0 1 13.8 21H9.5a5.96 5.96 0 0 0 1.49-3.98"></path></svg>
        <h5 class="card-title"> Fishing Forecast for:</h5>
        <h5 id="selectedFishName"></h5>
        <img class="fish-icon-large" id="selectedFishImage" src="" alt="Fish Display" />

      </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">Current Rating: ${weather_data.current_rating}</li>
          <li class="list-group-item">Dawn/Dusk Rating: ${weather_data.dawn_dusk_rating}</li>
          <li class="list-group-item">Morning/Evening Rating: ${weather_data.morning_evening_rating}</li>
          <li class="list-group-item">Tips for ${fish_species} today: Coming Soon! </li>
        </ul>
      </div>
              
      <!-- End of Fish Forecast Card -->
      `;
    })
  
      .catch(error => {
        console.error("Error sending location:", error);
        });
              
      });      
