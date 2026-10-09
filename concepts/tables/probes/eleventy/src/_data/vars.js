// The variables excerpt, read so pages use vars.name as in the source.
import { readFileSync } from "node:fs";
import yaml from "js-yaml";

export default yaml.load(readFileSync("../../source/template_variables.yml", "utf8")).template_variables;
