<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl = "http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" encoding="utf-8" />

<xsl:template match="/">
<html>
<head>
<title><xsl:value-of select="novx/PROJECT/Author" /></title>
</head>
<body>
<h1>
<xsl:value-of select="novx/PROJECT/Title" />
</h1>
<xsl:apply-templates select="novx/CHARACTERS" />
</body>
</html>
</xsl:template>

<xsl:template match="CHARACTER">
<h2>
<xsl:value-of select="Title" />
</h2>
<h3>Desc</h3>
<xsl:apply-templates select="Desc" />
<h3>Bio</h3>
<xsl:apply-templates select="Bio" />
<h3>Goals</h3>
<xsl:apply-templates select="Goals" />
</xsl:template>


<xsl:template match="p">
<p>
<xsl:apply-templates />
</p>
</xsl:template>


</xsl:stylesheet>
