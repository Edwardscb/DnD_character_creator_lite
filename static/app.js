const searchBar = document.getElementById('search-bar');
const searchButton = document.getElementById('search-button');
const search = document.getElementById('search');
const searchForm = document.getElementById('search-form')

search.addEventListener("click", (evt) => {
    evt.preventDefault();
    searchBar.classList.toggle('hidden')
    searchButton.classList.toggle('hidden')
    searchForm.classList.toggle('hidden')
})











// const statsDiv = document.getElementById("stats")
// const char_class = document.getElementById("character_class")




// const base_stats = () => {
//     // creates a vertical list of base stats and creates a dropdown selection from 1 to 18 for each stat
//     const stats = ['Strength', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma', 'Dexterity']
//     for (let stat of stats) {
//         let newDiv = document.createElement('div');
//         newDiv.innerText = `${stat}:  `;
//         newDiv.classList = 'newDiv';
//         newDiv.id = stat;
//         statsDiv.append(newDiv);
//         let contents = "<option>1</option>"
//         let newSelect = document.createElement('select');
//         newDiv.append(newSelect);
//         for (let i = 2; i < 19; i++) {
//             contents += "<option>" + i + "</option>";
//         }
//         newSelect.innerHTML = contents
//     }
    
// }


// adds event listener so that when the class changes, the hitpoints change....but don't need it anymore...
// char_class.addEventListener("change", (evt) => {
//     get_hit_die(evt.target.value);
//     console.log('test')
// })

//async fxn that will call the api to get the hit-die for the class that is chosen, might use this for exporting to pdf to calculate chosen max hit points
// async function get_hit_die(dice) {
//     classname = dice.toLowerCase()
//     resp = await axios.get(`https://www.dnd5eapi.co/api/classes/${classname}`)
//     dice_sides = resp.data.hit_die;
//     console.log('test1')
//     hitpoints(dice_sides)   
// }

//populates the dropdown menu with 1 to some number, depending on how high the hit-die goes...don't need anymore...
// function hitpoints(hitdie) {
//     console.log('test1.5')
//     defaultOption = document.getElementById("default-option");
//     let contents = "<option>1</option>"
//     for (let i = 2; i < hitdie+1; i++) {
//         contents += "<option>" + i + "</option>";      
//     }
//     defaultOption.innerHTML = contents;
//     console.log('test2')

// }

// async function hitpoints(hitdie) {

// }

// const hitpoints_default() {
    
// }
// async function get_weapons() {}
// async function get_armor() {}



