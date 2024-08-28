
    function addSection() {
        const container = document.getElementById('sections-container');
        const newSection = document.createElement('div');
        newSection.className = 'section';
    
        newSection.innerHTML = `
                    <div class="row">
                        <div class="col-lg-4">
                            <label for="given-name">Given Name:</label>
                            <input type="text" name="given-name" placeholder="Enter given name" required="True"/>
                        </div>
                        <div class="col-lg-4">
                            <label for="father-name">Father's Name:</label>
                            <input type="text" name="father-name" placeholder="Enter father's name" required="True"/>
                        </div>
                        <div class="col-lg-4">
                            <label for="grandfather-name">Grandfather's Name:</label>
                            <input type="text" name="grandfather-name" placeholder="Enter grandfather's name" required="True"/>
                        </div>
                       <div>
                            <i class="fas fa-trash delete-icon" onclick="deleteSection(this)"></i>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-lg-4">
                            <label for="dob">Date of Birth:</label>
                            <input type="date" name="dob" required="True"/>
                        </div>
                        <div class="col-lg-4">
                            <label for="gender">Gender:</label>
                            <select name="gender" required="True">
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                    </div>
        `;
    
        container.appendChild(newSection);
    }


    function deleteSection(icon) {
        const section = icon.closest('.section');
        section.remove();
    }

    
    
