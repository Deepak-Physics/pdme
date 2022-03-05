const pattern = /(\[tool\.poetry\]\nname = "pdme"\nversion = ")(?<vers>\d+\.\d+\.\d)(")/mg;

module.exports.readVersion = function (contents) {
	const result = pattern.exec(contents);
	return result.groups.vers;
}

module.exports.writeVersion = function (contents, version) {
	const newContents = contents.replace(pattern, `$1${version}$3`);
	return newContents;
}
