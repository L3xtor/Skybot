#include "nlohmann/json.hpp"
#include <fstream>
#include <iostream>
#include <string>

using json = nlohmann::json;

struct SkillInfo {
  int skill_level;
  double remaining_xp;
  double xp_required_to_level_up;
};

extern "C" SkillInfo getPlayerSkillInfo(double initial_exp,
                                        const char *skill_type,
                                        const char *json_path) {
  // Load JSON
  std::ifstream file(json_path);
  if (!file.is_open()) {
    std::cerr << "Error: Could not open file: " << json_path << "\n";
    return {0, 0, 0};
  }

  json json_data;
  try {
    file >> json_data;
  } catch (const json::parse_error &e) {
    std::cerr << "JSON parse error: " << e.what() << "\n";
    return {0, 0, 0};
  }

  // Extract sub-JSON (Skills or Catacombs)
  json selected_data;
  try {
    selected_data = json_data.at(skill_type);
  } catch (...) {
    std::cerr << "Invalid skill type: " << skill_type << "\n";
    return {0, 0, 0};
  }

  // Build lookup tables
  std::map<int, double> xp_required;
  std::map<int, double> cumulative_xp;

  for (auto &[level_str, values] : selected_data.items()) {
    int level = std::stoi(level_str);
    xp_required[level] = values[0];
    cumulative_xp[level] = values[1];
  }

  // Determine skill level
  int skill_level = 0;
  for (auto &[level, total_xp] : cumulative_xp) {
    if (initial_exp < total_xp) {
      skill_level = level - 1;
      break;
    }
  }

  // Clamp to max level if user exceeds it
  if (initial_exp >= cumulative_xp.rbegin()->second) {
    skill_level = cumulative_xp.rbegin()->first;
  }

  // Compute remaining XP
  double remaining_xp = initial_exp - cumulative_xp[skill_level];
  double xp_to_next = xp_required[skill_level + 1];

  return {skill_level, remaining_xp, xp_to_next};
}
