# Template and placeholder specifications for file export

Template-based file export: The application script iterates over chapters, sections, characters, locations, and items, selecting a template for each and replacing the placeholders with project data.

## List of templates

### Project level templates

- **fileHeader** (Text at the beginning of the exported file)
- **fileFooter** (Text at the end of the exported file)

### Chapter level templates

- **partTemplate** (chapter header; applied to chapters marked "section beginning")
- **chapterTemplate** (chapter header; applied to all "used" and "normal" chapters unless a "part template" exists)
- **unusedChapterTemplate** (chapter header; applied to chapters marked "unused")
- **chapterEndTemplate** (chapter footer; applied to all "used" and "normal" chapters unless a "part template" exists)
- **unusedChapterEndTemplate** (chapter footer; applied to chapters marked "unused")


### Section level templates

- **sectionTemplate** (applied to "used" sections within "normal" chapters)
- **firstSectionTemplate** (applied  to sections at the beginning of the chapter)
- **appendedSectionTemplate** (applied to sections marked "append to previous")
- **unusedSectionTemplate** (applied to "unused" sections)
- **sectionDivider** (lead sections, beginning from the second in chapter)


### World building templates

- **characterSectionHeading** (precedes the characters)
- **characterTemplate** (applied to each character)
- **locationSectionHeading** (precedes the locations)
- **locationTemplate** (applied to each location)
- **itemSectionHeading** (precedes the items)
- **itemTemplate** (applied to each item)



## Placeholders

### Syntax

There are two options:

1. `$Placeholder` -- If the placeholder is followed by a character that is clearly recognizable as a separator, e.g. a blank. 
2. `${Placeholder}` -- If the placeholder is followed by a character that is not recognizable as a separator.


### "Project template" placeholders

- **$Title** - Project title
- **$Desc** - Project description
- **$AuthorName** - Author's name
- **$Language** - Language code acc. to ISO 639-1
- **$Country** - Country code acc. to ISO 3166-2
- **$CustomPlotProgress** - Custom "Plot progress" field title
- **$CustomCharacterization** - Custom "Characterization" field title
- **$CustomWorldBuilding** - Custom "World building" field title
- **$CustomGoal** - Custom "Goal" field title
- **$CustomConflict** - Custom "Conflict" field title
- **$CustomOutcome** - Custom "Outcome" field title
- **$CustomChrBio** - Custom character "Bio" field title
- **$CustomChrGoals** - Custom character "Goals" field title

### "Chapter template" placeholders

- **$ID** - Chapter ID,
- **$ChapterNumber** - Chapter number (in sort order),
- **$Title** - Chapter title
- **$Desc** - Chapter description
- **$Notes** - Chapter notes
- **$ProjectName** - URL-coded file name without suffix and extension
- **$ProjectPath** - URL-coded fpath to the project directory
- **$Language** - Language code acc. to ISO 639-1
- **$Country** - Country code acc. to ISO 3166-2
- **$ManuscriptSuffix** - File name suffix of the manuscript

### "Section template" placeholders

- **$ID** - Section ID,
- **$SectionNumber** - Section number (in sort order),
- **$Title** - Section title
- **$Desc** - Section description
- **$WordCount** - Section word count
- **$WordsTotal** - Accumulated word count including the current section
- **$Status** - Section status (Outline, Draft etc.)
- **$SectionContent** - Section content
- **$Date** - Specific section date (yyyy-mm-dd)
- **$Time** - Time section begins: (hh:mm)
- **$OdsTime** - Time section begins: (PThhHmmMssS)
- **$Day** - Day section begins
- **$ScDate** - Date or day (localized)
- **$DateYear** - Year
- **$DateMonth** - Month (number)
- **$DateDay** - Day (number)
- **$DateWeekday** - Day of the week (name)
- **$MonthName** - Month (name)
- **$LastsDays** - Amount of time section lasts: days
- **$LastsHours** - Amount of time section lasts: hours
- **$LastsMinutes** - Amount of time section lasts: minutes
- **Duration** - Combination of days and hours and minutes
- **$Scene** - The sections's kind of scene, if any
- **$Goal** - The section protagonist's goal
- **$Conflict** - The section conflict
- **$Outcome** - The section outcome
- **$Tags** - Comma-separated list of section tags
- **$Characters** - Comma-separated list of characters assigned to the section
- **$Viewpoint** - Viewpoint character
- **$Locations** - Comma-separated list of locations assigned to the section
- **$Items** - Comma-separated list of items assigned to the section
- **$Notes** - Section notes
- **$ProjectName** - URL-coded file name without suffix and extension
- **$ProjectPath** - URL-coded fpath to the project directory
- **$Language** - Language code acc. to ISO 639-1
- **$Country** - Country code acc. to ISO 3166-2
- **$ManuscriptSuffix** - File name suffix of the manuscript
- **$SectionsSuffix** - File name suffix of the section descriptions
- **$CustomPlotProgress** - Custom "Plot progress" field title
- **$CustomCharacterization** - Custom "Characterization" field title
- **$CustomWorldBuilding** - Custom "World building" field title
- **$CustomGoal** - Custom "Goal" field title
- **$CustomConflict** - Custom "Conflict" field title
- **$CustomOutcome** - Custom "Outcome" field title


### "Character template" placeholders

- **$ID** - Character ID
- **$Title** - Character's name
- **$Desc** - Character description
- **$Tags** - Character tags
- **$AKA** - Alternative name
- **$Notes** - Character notes
- **$Bio** - The character's biography
- **$Goals** - The character's goals in the story
- **$FullName** - Character's full name)
- **$Status** - Major/minor character
- **$ProjectName** - URL-coded file name without suffix and extension
- **$ProjectPath** - URL-coded fpath to the project directory
- **$CharactersSuffix** - File name suffix of the character descriptions
- **$CustomChrBio** - Custom character "Bio" field title
- **$CustomChrGoals** - Custom character "Goals" field title

### "Location template" placeholders

- **$ID** - Location ID
- **$Title** - Location's name
- **$Desc** - Location description
- **$Notes** - location notes
- **$Tags** - Location tags
- **$AKA** - Alternative name
- **$ProjectName** - URL-coded file name without suffix and extension
- **$ProjectPath** - URL-coded fpath to the project directory
- **$LocationsSuffix** - File name suffix of the character descriptions

### "Item template" placeholders

- **$ID** - Item ID
- **$Title** - Item's name
- **$Desc** - Item description
- **$Notes** - Item notes
- **$Tags** - Item tags
- **$AKA** - Alternative name
- **$ProjectName** - URL-coded file name without suffix and extension
- **$ProjectPath** - URL-coded fpath to the project directory
- **$ItemsSuffix** - File name suffix of the character descriptions


### "Plot line" placeholders

- **$ID** - Plot line ID,
- **$Title** - Plot line title
- **$Desc** - Plot line description
- **$Notes** - Plot line notes
- **$ProjectName** - URL-coded file name without suffix and extension
- **$ProjectPath** - URL-coded fpath to the project directory
- **$Language** - Language code acc. to ISO 639-1
- **$Country** - Country code acc. to ISO 3166-2

### "Project notes" placeholders

- **$ID** - Project notes ID,
- **$Title** - Project notes title
- **$Desc** - Project notes content
- **$ProjectName** - URL-coded file name without suffix and extension
- **$ProjectPath** - URL-coded fpath to the project directory
