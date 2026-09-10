-- Table cells retain all content; landscape gives matrix ledgers room to breathe.
function Pandoc(doc)
  local out = pandoc.List()
  local appendix = false
  local function raw(s) out:insert(pandoc.RawBlock('latex',s)) end
  for _,block in ipairs(doc.blocks) do
    if block.t == 'Header' and block.level <= 2 then
      if appendix then raw('\\end{landscape}'); appendix=false end
      if pandoc.utils.stringify(block):find('模型矩阵查阅表') then
        raw('\\begin{landscape}'); appendix=true
      end
    end
    if block.t == 'Table' then
      local wide = #block.colspecs >= 5 and not appendix
      if wide then
        -- Keep a short table heading on the table page, not the previous page.
        local previous=out[#out]
        if previous and previous.t=='Para' and previous.content[1] and previous.content[1].t=='Strong'
            and #pandoc.utils.stringify(previous)<220 then
          out:remove(#out);raw('\\begin{landscape}');out:insert(previous)
        else raw('\\begin{landscape}') end
      end
      raw('\\begin{infratable}');out:insert(block);raw('\\end{infratable}')
      if wide then raw('\\end{landscape}') end
    else out:insert(block) end
  end
  if appendix then raw('\\end{landscape}') end
  doc.blocks=out
  return doc
end
function Math(el)
  -- Keep Greek mu in math mode; \mathrm text fonts lack its math Unicode glyph.
  el.text = el.text:gsub('\\mathrm{%s*\\mu%s*s}', '\\mu\\,\\mathrm{s}')
  if el.mathtype == 'DisplayMath' then
    if el.text:find('\\tag',1,true) then return el end
    return pandoc.RawInline('latex', '\\begin{infraequation}' .. el.text .. '\\end{infraequation}')
  end
  return el
end
function Header(el)
  if el.level > 1 and not pandoc.utils.stringify(el):match('^%d') then
    el.classes:insert('unnumbered')
  end
  -- Source numbers are removed only after deciding whether it is a numbered heading.
  local inlines = el.content
  if el.level == 1 then
    -- Preprocessor has removed the Chinese chapter prefix.
    return el
  end
  if inlines[1] and inlines[1].t == 'Str' and inlines[1].text:match('^%d+%.') then
    inlines:remove(1)
    if inlines[1] and inlines[1].t == 'Space' then inlines:remove(1) end
  end
  return el
end
