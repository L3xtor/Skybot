#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp>
#include <string>

using namespace std;
using json = nlohmann::json;

// Global JSON objects
json json_data;
json xp_required, cumulative_xp_required;

// Creating structure for player's skill
struct SkillInfo {
    int skill_level;
    double remaining_xp;
    double xp_required_to_level_up;
};

// Function to initialize JSON based on user input
extern "C" void get_skill_info(const char skill_type[15]) {
    ifstream file("./hypixel/catacombs/utils/json/skill_levels.json");

    if (!file.is_open()) {
        cerr << "Error: Could not open the file." << endl;
        exit(1);  // Terminate the program if the file cannot be opened
    }

    try {
        file >> json_data;

        // Determine whether the user wants "Skills" or "Catacombs"
        json selected_data = json_data[skill_type];

        // Populate xp_required and cumulative_xp_required
        for (auto& [level, values] : selected_data.items()) {
            xp_required[level] = values[0];          // First column (XP required to level up)
            cumulative_xp_required[level] = values[1]; // Second column (Total XP needed to reach that level)
        }

    } catch (json::parse_error& e) {
        cerr << "JSON parse error: " << e.what() << endl;
        exit(1);  // Terminate the program if there's a JSON parse error
    }
}

// Function to find the skill level by XP
extern "C" int find_skill_level(int skill_xp) {
    // Iterate over each key-value pair in the JSON object
    for (auto& [skill, xp_needed] : cumulative_xp_required.items()) {
        // Check if the value matches the value you're looking for
        if (xp_needed >= skill_xp) {
            return stoi(skill) - 1;  // Convert key (string) to int and return
        }
    }
    return 0;
}

// Function to find the remaining XP after leveling up
extern "C" double find_remaining_xp(double initial_exp, string skill_level) {
    // Iterate over each skill and cumulative xp required
    double remaining_xp = initial_exp - (double)cumulative_xp_required[skill_level];

    return remaining_xp;
}

// Function to get XP required to level up
extern "C" double calculate_xp_to_level_up(int skill_level) {
    for (auto& [skill, xp] : cumulative_xp_required.items()) {
        if (skill_level == (stoi(skill) + 1)) return xp;
    }
    return 0;
}

// Function to check XP and return remaining XP and skill level
extern "C" SkillInfo getPlayerSkillInfo(double initial_exp, const char skill_name[15]) {

    // Initialize variables to return
    double remaining_xp = 0, xp_required_to_level_up = 0;
    int skill_level = 0;

    // Get level of either Catacombs or other skills
    get_skill_info(skill_name);

    // Iterate over each skill level and return the required data needed
    for (size_t exp : cumulative_xp_required) {
        if (exp >= initial_exp) {
            skill_level = find_skill_level(initial_exp);
            remaining_xp = find_remaining_xp(initial_exp, to_string(skill_level));
            xp_required_to_level_up = calculate_xp_to_level_up(skill_level);
            break;
        }
    }

    // Returning the data
    return {skill_level, remaining_xp, xp_required_to_level_up};
}
