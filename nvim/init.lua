-- lazy.nvim kurulumu
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({ "git", "clone", "--filter=blob:none", "https://github.com/folke/lazy.nvim.git", "--branch=stable", lazypath })
end
vim.opt.rtp:prepend(lazypath)

-- GENEL AYARLAR
vim.g.mapleader = " "
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.termguicolors = true
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true
vim.opt.mouse = "a" -- Fare desteği

-- EKLENTİ LİSTESİ
require("lazy").setup({
  -- 1. TEMA VE ŞEFFAFLIK
  {
    "catppuccin/nvim",
    name = "catppuccin",
    priority = 1000,
    config = function()
      require("catppuccin").setup({
        transparent_background = true, -- Şeffaflığı açar
        color_overrides = {
          all = {
            base = "#1E1D2F",
            mantle = "#1E1D2F",
            crust = "#1E1D2F",
            text = "#D9E0EE",
            blue = "#5DBB63",
            pink = "#F28FAD",
          },
        },
      })
      vim.cmd.colorscheme "catppuccin"
      
      -- 0.85 Şeffaflık ayarı (Terminal üzerinden gelen şeffaflığı korur)
      vim.api.nvim_set_hl(0, "Normal", { bg = "none" })
      vim.api.nvim_set_hl(0, "NormalFloat", { bg = "none" })
    end,
  },

  -- 2. TELESCOPE (Dosya ve Kelime Arama - İnternetteki en popüler plugin)
  {
    'nvim-telescope/telescope.nvim', tag = '0.1.5',
    dependencies = { 'nvim-lua/plenary.nvim' },
    config = function()
      local builtin = require('telescope.builtin')
      vim.keymap.set('n', '<leader>ff', builtin.find_files, {}) -- Space+ff dosya arar
      vim.keymap.set('n', '<leader>fg', builtin.live_grep, {})  -- Space+fg kelime arar
    end
  },

  -- 3. LUALINE (Alt Bar - Renk paletinle uyumlu)
  {
    'nvim-lualine/lualine.nvim',
    dependencies = { 'nvim-tree/nvim-web-devicons' },
    config = function() require('lualine').setup({ options = { theme = 'catppuccin' } }) end
  },

  -- 4. FILE TREE (Dosya Gezgini)
  {
    "nvim-tree/nvim-tree.lua",
    config = function()
      require("nvim-tree").setup()
      vim.keymap.set('n', '<leader>e', ':NvimTreeToggle<CR>')
    end,
  },

  -- 5. AUTO PAIRS (Parantezleri otomatik kapatır)
  { "windwp/nvim-autopairs", config = function() require("nvim-autopairs").setup {} end },

  -- 6. COMMENT.NVIM (Kodları hızlıca yorum satırı yapar)
  { "numToStr/Comment.nvim", config = function() require("Comment").setup() end },

  -- 7. BUFFERLINE (Üstte sekmeler/tablar)
  {
    'akinsho/bufferline.nvim',
    version = "*",
    dependencies = 'nvim-tree/nvim-web-devicons',
    config = function() require("bufferline").setup{} end
  },

  -- 8. KOD TAMAMLAMA (Autocomplete & Snippets)
  { "neovim/nvim-lspconfig" },
  { "williamboman/mason.nvim", config = true },
  { "williamboman/mason-lspconfig.nvim", config = true },
  {
    "hrsh7th/nvim-cmp",
    dependencies = {
      "hrsh7th/cmp-nvim-lsp",
      "L3MON4D3/LuaSnip",
      "saadparwaiz1/cmp_luasnip",
      "rafamadriz/friendly-snippets",
    },
    config = function()
      local cmp = require("cmp")
      cmp.setup({
        snippet = { expand = function(args) require("luasnip").lsp_expand(args.body) end },
        mapping = cmp.mapping.preset.insert({
          ['<Tab>'] = cmp.mapping.select_next_item(),
          ['<CR>'] = cmp.mapping.confirm({ select = true }),
        }),
        sources = cmp.config.sources({ { name = 'nvim_lsp' }, { name = 'luasnip' } })
      })
    end,
  },
})
