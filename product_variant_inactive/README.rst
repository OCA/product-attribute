<!DOCTYPE html>
<html lang="en" class="">
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="Content-Language" content="en">


    <title>maintainer-tools/README.rst at master · OCA/maintainer-tools</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub">
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub">
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png">
    <meta property="fb:app_id" content="1401488693436528">

      <meta content="@github" name="twitter:site" /><meta content="summary" name="twitter:card" /><meta content="OCA/maintainer-tools" name="twitter:title" /><meta content="maintainer-tools - Odoo Maintainers Tools for OCA members which evaluate and maintain repositories." name="twitter:description" /><meta content="https://avatars1.githubusercontent.com/u/7600578?v=3&amp;s=400" name="twitter:image:src" />
      <meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="https://avatars1.githubusercontent.com/u/7600578?v=3&amp;s=400" property="og:image" /><meta content="OCA/maintainer-tools" property="og:title" /><meta content="https://github.com/OCA/maintainer-tools" property="og:url" /><meta content="maintainer-tools - Odoo Maintainers Tools for OCA members which evaluate and maintain repositories." property="og:description" />
      <meta name="browser-stats-url" content="https://api.github.com/_private/browser/stats">
    <meta name="browser-errors-url" content="https://api.github.com/_private/browser/errors">
    <link rel="assets" href="https://assets-cdn.github.com/">
    <link rel="web-socket" href="wss://live.github.com/_sockets/MTEzMjkxMjY6OGVjOWIzYzE3ZDEzNTU1OGFlOTJiZWRlYTEyNDY5MGE6YzZkOGQ3NDc1Zjk1Nzg2MDA3YmZjYTk0ZmFkYTVmMDlhMzE3YWVkMDUxZTdmYmNhYTZhM2NiNmRkYTYxNjM1Yw==--c1a44ebf7f8e1c8f66b0036522dab384d346d524">
    <meta name="pjax-timeout" content="1000">
    <link rel="sudo-modal" href="/sessions/sudo_modal">

    <meta name="msapplication-TileImage" content="/windows-tile.png">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="selected-link" value="repo_source" data-pjax-transient>
      <meta name="google-analytics" content="UA-3769691-2">

    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="6DBE793B:0C0A:1D4A3F32:555083CB" name="octolytics-dimension-request_id" /><meta content="11329126" name="octolytics-actor-id" /><meta content="ahilali" name="octolytics-actor-login" /><meta content="79e1890ac86be0753e42b03d1eb4be61b05b2e818e83959557eea744917731dd" name="octolytics-actor-hash" />
    
    <meta content="Rails, view, blob#show" name="analytics-event" />
    <meta class="js-ga-set" name="dimension1" content="Logged In">
    <meta class="js-ga-set" name="dimension2" content="Header v3">
    <meta name="is-dotcom" content="true">
    <meta name="hostname" content="github.com">
    <meta name="user-login" content="ahilali">

    
    <link rel="icon" type="image/x-icon" href="https://assets-cdn.github.com/favicon.ico">


    <meta content="authenticity_token" name="csrf-param" />
<meta content="er3VatbOpNbG0dCXXAVv85p7vGAlZ43AvCGBNqKEWOmZCE1Hred+EEIJrTimGH3z5CGElOJC2WDYHxt0PmgGjw==" name="csrf-token" />

    <link href="https://assets-cdn.github.com/assets/github-c486157afcc5f58155a921bc675afb08733fbaa8dcf39ac2104d381dd9c82ac2.css" media="all" rel="stylesheet" />
    <link href="https://assets-cdn.github.com/assets/github2-da2e842cc3f0aaf33b727d0ef034243c12ab008fd09b24868b97719683b40ee7.css" media="all" rel="stylesheet" />
    
    


    <meta http-equiv="x-pjax-version" content="4426702614c8182f33d1780ad1169662">

      
  <meta name="description" content="maintainer-tools - Odoo Maintainers Tools for OCA members which evaluate and maintain repositories.">
  <meta name="go-import" content="github.com/OCA/maintainer-tools git https://github.com/OCA/maintainer-tools.git">

  <meta content="7600578" name="octolytics-dimension-user_id" /><meta content="OCA" name="octolytics-dimension-user_login" /><meta content="20999008" name="octolytics-dimension-repository_id" /><meta content="OCA/maintainer-tools" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="20999008" name="octolytics-dimension-repository_network_root_id" /><meta content="OCA/maintainer-tools" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/OCA/maintainer-tools/commits/master.atom" rel="alternate" title="Recent Commits to maintainer-tools:master" type="application/atom+xml">

  </head>


  <body class="logged_in  env-production linux vis-public page-blob">
    <a href="#start-of-content" tabindex="1" class="accessibility-aid js-skip-to-content">Skip to content</a>
    <div class="wrapper">
      
      
      


        <div class="header header-logged-in true" role="banner">
  <div class="container clearfix">

    <a class="header-logo-invertocat" href="https://github.com/" data-hotkey="g d" aria-label="Homepage" data-ga-click="Header, go to dashboard, icon:logo">
  <span class="mega-octicon octicon-mark-github"></span>
</a>


      <div class="site-search repo-scope js-site-search" role="search">
          <form accept-charset="UTF-8" action="/OCA/maintainer-tools/search" class="js-site-search-form" data-global-search-url="/search" data-repo-search-url="/OCA/maintainer-tools/search" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
  <input type="text"
    class="js-site-search-field is-clearable"
    data-hotkey="s"
    name="q"
    placeholder="Search"
    data-global-scope-placeholder="Search GitHub"
    data-repo-scope-placeholder="Search"
    tabindex="1"
    autocapitalize="off">
  <div class="scope-badge">This repository</div>
</form>
      </div>

      <ul class="header-nav left" role="navigation">
          <li class="header-nav-item explore">
            <a class="header-nav-link" href="/explore" data-ga-click="Header, go to explore, text:explore">Explore</a>
          </li>
            <li class="header-nav-item">
              <a class="header-nav-link" href="https://gist.github.com" data-ga-click="Header, go to gist, text:gist">Gist</a>
            </li>
            <li class="header-nav-item">
              <a class="header-nav-link" href="/blog" data-ga-click="Header, go to blog, text:blog">Blog</a>
            </li>
          <li class="header-nav-item">
            <a class="header-nav-link" href="https://help.github.com" data-ga-click="Header, go to help, text:help">Help</a>
          </li>
      </ul>

      
<ul class="header-nav user-nav right" id="user-links">
  <li class="header-nav-item dropdown js-menu-container">
    <a class="header-nav-link name" href="/ahilali" data-ga-click="Header, go to profile, text:username">
      <img alt="@ahilali" class="avatar" data-user="11329126" height="20" src="https://avatars1.githubusercontent.com/u/11329126?v=3&amp;s=40" width="20" />
      <span class="css-truncate">
        <span class="css-truncate-target">ahilali</span>
      </span>
    </a>
  </li>

  <li class="header-nav-item dropdown js-menu-container">
    <a class="header-nav-link js-menu-target tooltipped tooltipped-s" href="/new" aria-label="Create new..." data-ga-click="Header, create new, icon:add">
      <span class="octicon octicon-plus"></span>
      <span class="dropdown-caret"></span>
    </a>

    <div class="dropdown-menu-content js-menu-content">
      <ul class="dropdown-menu">
        
<li>
  <a href="/new" data-ga-click="Header, create new repository, icon:repo"><span class="octicon octicon-repo"></span> New repository</a>
</li>
<li>
  <a href="/organizations/new" data-ga-click="Header, create new organization, icon:organization"><span class="octicon octicon-organization"></span> New organization</a>
</li>


  <li class="dropdown-divider"></li>
  <li class="dropdown-header">
    <span title="OCA/maintainer-tools">This repository</span>
  </li>
    <li>
      <a href="/OCA/maintainer-tools/issues/new" data-ga-click="Header, create new issue, icon:issue"><span class="octicon octicon-issue-opened"></span> New issue</a>
    </li>

      </ul>
    </div>
  </li>

  <li class="header-nav-item">
      <span class="js-socket-channel js-updatable-content"
        data-channel="notification-changed:ahilali"
        data-url="/notifications/header">
      <a href="/notifications" aria-label="You have unread notifications" class="header-nav-link notification-indicator tooltipped tooltipped-s" data-ga-click="Header, go to notifications, icon:unread" data-hotkey="g n">
          <span class="mail-status unread"></span>
          <span class="octicon octicon-inbox"></span>
</a>  </span>

  </li>

  <li class="header-nav-item">
    <a class="header-nav-link tooltipped tooltipped-s" href="/settings/profile" id="account_settings" aria-label="Settings" data-ga-click="Header, go to settings, icon:settings">
      <span class="octicon octicon-gear"></span>
    </a>
  </li>

  <li class="header-nav-item">
    <form accept-charset="UTF-8" action="/logout" class="logout-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="8dBgdMDBFSTrf0nVs6Wr43ITwErk81rmsQ/Rkyp/7mj9CwY6aojzJw7quWB+J8+cJMESCcKTUeY9TsWgNdO6CA==" /></div>
      <button class="header-nav-link sign-out-button tooltipped tooltipped-s" aria-label="Sign out" data-ga-click="Header, sign out, icon:logout">
        <span class="octicon octicon-sign-out"></span>
      </button>
</form>  </li>

</ul>



    
  </div>
</div>

        

        


      <div id="start-of-content" class="accessibility-aid"></div>
          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    <div id="js-flash-container">
      
    </div>
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">
        
<ul class="pagehead-actions">

  <li>
      <form accept-charset="UTF-8" action="/notifications/subscribe" class="js-social-container" data-autosubmit="true" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="RlYulxbE6hKehFcNzlAtq1ggS6Vij649wAkyBtascnLPwkp0ObOQackw133JNG5Z8+Qr1yRIzsCSeJ2PTLP2cQ==" /></div>    <input id="repository_id" name="repository_id" type="hidden" value="20999008" />

      <div class="select-menu js-menu-container js-select-menu">
        <a href="/OCA/maintainer-tools/subscription"
          class="btn btn-sm btn-with-count select-menu-button js-menu-target" role="button" tabindex="0" aria-haspopup="true"
          data-ga-click="Repository, click Watch settings, action:blob#show">
          <span class="js-select-button">
            <span class="octicon octicon-eye"></span>
            Watch
          </span>
        </a>
        <a class="social-count js-social-count" href="/OCA/maintainer-tools/watchers">
          32
        </a>

        <div class="select-menu-modal-holder">
          <div class="select-menu-modal subscription-menu-modal js-menu-content" aria-hidden="true">
            <div class="select-menu-header">
              <span class="select-menu-title">Notifications</span>
              <span class="octicon octicon-x js-menu-close" role="button" aria-label="Close"></span>
            </div>

            <div class="select-menu-list js-navigation-container" role="menu">

              <div class="select-menu-item js-navigation-item selected" role="menuitem" tabindex="0">
                <span class="select-menu-item-icon octicon octicon-check"></span>
                <div class="select-menu-item-text">
                  <input checked="checked" id="do_included" name="do" type="radio" value="included" />
                  <span class="select-menu-item-heading">Not watching</span>
                  <span class="description">Be notified when participating or @mentioned.</span>
                  <span class="js-select-button-text hidden-select-button-text">
                    <span class="octicon octicon-eye"></span>
                    Watch
                  </span>
                </div>
              </div>

              <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
                <span class="select-menu-item-icon octicon octicon octicon-check"></span>
                <div class="select-menu-item-text">
                  <input id="do_subscribed" name="do" type="radio" value="subscribed" />
                  <span class="select-menu-item-heading">Watching</span>
                  <span class="description">Be notified of all conversations.</span>
                  <span class="js-select-button-text hidden-select-button-text">
                    <span class="octicon octicon-eye"></span>
                    Unwatch
                  </span>
                </div>
              </div>

              <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
                <span class="select-menu-item-icon octicon octicon-check"></span>
                <div class="select-menu-item-text">
                  <input id="do_ignore" name="do" type="radio" value="ignore" />
                  <span class="select-menu-item-heading">Ignoring</span>
                  <span class="description">Never be notified.</span>
                  <span class="js-select-button-text hidden-select-button-text">
                    <span class="octicon octicon-mute"></span>
                    Stop ignoring
                  </span>
                </div>
              </div>

            </div>

          </div>
        </div>
      </div>
</form>
  </li>

  <li>
    
  <div class="js-toggler-container js-social-container starring-container ">

    <form accept-charset="UTF-8" action="/OCA/maintainer-tools/unstar" class="js-toggler-form starred js-unstar-button" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="cbFCNjw+pGuWy+hUp1cROCOAEXsrdhI9l1z980SwKudOk9aba6F9+RX0kYshJaV/zsXEf782cjhxDx/rmiEhQQ==" /></div>
      <button
        class="btn btn-sm btn-with-count js-toggler-target"
        aria-label="Unstar this repository" title="Unstar OCA/maintainer-tools"
        data-ga-click="Repository, click unstar button, action:blob#show; text:Unstar">
        <span class="octicon octicon-star"></span>
        Unstar
      </button>
        <a class="social-count js-social-count" href="/OCA/maintainer-tools/stargazers">
          11
        </a>
</form>
    <form accept-charset="UTF-8" action="/OCA/maintainer-tools/star" class="js-toggler-form unstarred js-star-button" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="0BfznfXR5FO3dFs5TxSNACRhA8i8ZMCWQ8Ojr6BZVJQkXlmJANNoVLZYdFpKFT1SXyKzmI310OZuakNKvFU8NQ==" /></div>
      <button
        class="btn btn-sm btn-with-count js-toggler-target"
        aria-label="Star this repository" title="Star OCA/maintainer-tools"
        data-ga-click="Repository, click star button, action:blob#show; text:Star">
        <span class="octicon octicon-star"></span>
        Star
      </button>
        <a class="social-count js-social-count" href="/OCA/maintainer-tools/stargazers">
          11
        </a>
</form>  </div>

  </li>

        <li>
          <a href="#fork-destination-box" class="btn btn-sm btn-with-count"
              title="Fork your own copy of OCA/maintainer-tools to your account"
              aria-label="Fork your own copy of OCA/maintainer-tools to your account"
              rel="facebox"
              data-ga-click="Repository, show fork modal, action:blob#show; text:Fork">
            <span class="octicon octicon-repo-forked"></span>
            Fork
          </a>
          <a href="/OCA/maintainer-tools/network" class="social-count">32</a>

          <div id="fork-destination-box" style="display: none;">
            <h2 class="facebox-header">Where should we fork this repository?</h2>
            <include-fragment src=""
                class="js-fork-select-fragment fork-select-fragment"
                data-url="/OCA/maintainer-tools/fork?fragment=1">
              <img alt="Loading" height="64" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-128-338974454bb5c32803e82f601beb051d373744b024fe8742a76009700fd7e033.gif" width="64" />
            </include-fragment>
          </div>
        </li>

</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="mega-octicon octicon-repo"></span>
          <span class="author"><a href="/OCA" class="url fn" itemprop="url" rel="author"><span itemprop="title">OCA</span></a></span><!--
       --><span class="path-divider">/</span><!--
       --><strong><a href="/OCA/maintainer-tools" class="js-current-repository" data-pjax="#js-repo-pjax-container">maintainer-tools</a></strong>

          <span class="page-context-loader">
            <img alt="" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
          </span>

        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    <div class="container">
      <div class="repository-with-sidebar repo-container new-discussion-timeline  ">
        <div class="repository-sidebar clearfix">
            
<nav class="sunken-menu repo-nav js-repo-nav js-sidenav-container-pjax js-octicon-loaders"
     role="navigation"
     data-pjax="#js-repo-pjax-container"
     data-issue-count-url="/OCA/maintainer-tools/issues/counts">
  <ul class="sunken-menu-group">
    <li class="tooltipped tooltipped-w" aria-label="Code">
      <a href="/OCA/maintainer-tools" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-hotkey="g c" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches /OCA/maintainer-tools">
        <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
        <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
</a>    </li>

      <li class="tooltipped tooltipped-w" aria-label="Issues">
        <a href="/OCA/maintainer-tools/issues" aria-label="Issues" class="js-selected-navigation-item sunken-menu-item" data-hotkey="g i" data-selected-links="repo_issues repo_labels repo_milestones /OCA/maintainer-tools/issues">
          <span class="octicon octicon-issue-opened"></span> <span class="full-word">Issues</span>
          <span class="js-issue-replace-counter"></span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
</a>      </li>

    <li class="tooltipped tooltipped-w" aria-label="Pull requests">
      <a href="/OCA/maintainer-tools/pulls" aria-label="Pull requests" class="js-selected-navigation-item sunken-menu-item" data-hotkey="g p" data-selected-links="repo_pulls /OCA/maintainer-tools/pulls">
          <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull requests</span>
          <span class="js-pull-replace-counter"></span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
</a>    </li>

      <li class="tooltipped tooltipped-w" aria-label="Wiki">
        <a href="/OCA/maintainer-tools/wiki" aria-label="Wiki" class="js-selected-navigation-item sunken-menu-item" data-hotkey="g w" data-selected-links="repo_wiki /OCA/maintainer-tools/wiki">
          <span class="octicon octicon-book"></span> <span class="full-word">Wiki</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
</a>      </li>
  </ul>
  <div class="sunken-menu-separator"></div>
  <ul class="sunken-menu-group">

    <li class="tooltipped tooltipped-w" aria-label="Pulse">
      <a href="/OCA/maintainer-tools/pulse" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-selected-links="pulse /OCA/maintainer-tools/pulse">
        <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
        <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
</a>    </li>

    <li class="tooltipped tooltipped-w" aria-label="Graphs">
      <a href="/OCA/maintainer-tools/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-selected-links="repo_graphs repo_contributors /OCA/maintainer-tools/graphs">
        <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
        <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/assets/spinners/octocat-spinner-32-e513294efa576953719e4e2de888dd9cf929b7d62ed8d05f25e731d02452ab6c.gif" width="16" />
</a>    </li>
  </ul>


</nav>

              <div class="only-with-full-nav">
                  
<div class="clone-url "
  data-protocol-type="http"
  data-url="/users/set_protocol?protocol_selector=http&amp;protocol_type=clone">
  <h3><span class="text-emphasized">HTTPS</span> clone URL</h3>
  <div class="input-group js-zeroclipboard-container">
    <input type="text" class="input-mini input-monospace js-url-field js-zeroclipboard-target"
           value="https://github.com/OCA/maintainer-tools.git" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>

  
<div class="clone-url open"
  data-protocol-type="ssh"
  data-url="/users/set_protocol?protocol_selector=ssh&amp;protocol_type=clone">
  <h3><span class="text-emphasized">SSH</span> clone URL</h3>
  <div class="input-group js-zeroclipboard-container">
    <input type="text" class="input-mini input-monospace js-url-field js-zeroclipboard-target"
           value="git@github.com:OCA/maintainer-tools.git" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>

  
<div class="clone-url "
  data-protocol-type="subversion"
  data-url="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=clone">
  <h3><span class="text-emphasized">Subversion</span> checkout URL</h3>
  <div class="input-group js-zeroclipboard-container">
    <input type="text" class="input-mini input-monospace js-url-field js-zeroclipboard-target"
           value="https://github.com/OCA/maintainer-tools" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>



<p class="clone-options">You can clone with
  <a href="#" class="js-clone-selector" data-protocol="http">HTTPS</a>, <a href="#" class="js-clone-selector" data-protocol="ssh">SSH</a>, or <a href="#" class="js-clone-selector" data-protocol="subversion">Subversion</a>.
  <a href="https://help.github.com/articles/which-remote-url-should-i-use" class="help tooltipped tooltipped-n" aria-label="Get help on which URL is right for you.">
    <span class="octicon octicon-question"></span>
  </a>
</p>




                <a href="/OCA/maintainer-tools/archive/master.zip"
                   class="btn btn-sm sidebar-button"
                   aria-label="Download the contents of OCA/maintainer-tools as a zip file"
                   title="Download the contents of OCA/maintainer-tools as a zip file"
                   rel="nofollow">
                  <span class="octicon octicon-cloud-download"></span>
                  Download ZIP
                </a>
              </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>

          

<a href="/OCA/maintainer-tools/blob/ef7da4f13d2b8f9f0f3dd0a36c1a27622f777f08/template/module/README.rst" class="hidden js-permalink-shortcut" data-hotkey="y">Permalink</a>

<!-- blob contrib key: blob_contributors:v21:796154a1f9681204d3d4b949eafd3af4 -->

<div class="file-navigation js-zeroclipboard-container">
  
<div class="select-menu js-menu-container js-select-menu left">
  <span class="btn btn-sm select-menu-button js-menu-target css-truncate" data-hotkey="w"
    data-master-branch="master"
    data-ref="master"
    title="master"
    role="button" aria-label="Switch branches or tags" tabindex="0" aria-haspopup="true">
    <span class="octicon octicon-git-branch"></span>
    <i>branch:</i>
    <span class="js-select-button css-truncate-target">master</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax aria-hidden="true">

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-x js-menu-close" role="button" aria-label="Close"></span>
      </div>

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Filter branches/tags" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" data-filter-placeholder="Filter branches/tags" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" data-filter-placeholder="Find a tag…" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div>
      </div>
      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">
            <a class="select-menu-item js-navigation-item js-navigation-open selected"
               href="/OCA/maintainer-tools/blob/master/template/module/README.rst"
               data-name="master"
               data-skip-pjax="true"
               rel="nofollow">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <span class="select-menu-item-text css-truncate-target" title="master">
                master
              </span>
            </a>
        </div>

          <div class="select-menu-no-results">Nothing to show</div>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div>

    </div>
  </div>
</div>

  <div class="btn-group right">
    <a href="/OCA/maintainer-tools/find/master"
          class="js-show-file-finder btn btn-sm empty-icon tooltipped tooltipped-s"
          data-pjax
          data-hotkey="t"
          aria-label="Quickly jump between files">
      <span class="octicon octicon-list-unordered"></span>
    </a>
    <button aria-label="Copy file path to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
  </div>

  <div class="breadcrumb js-zeroclipboard-target">
    <span class='repo-root js-repo-root'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/OCA/maintainer-tools" class="" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">maintainer-tools</span></a></span></span><span class="separator">/</span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/OCA/maintainer-tools/tree/master/template" class="" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">template</span></a></span><span class="separator">/</span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/OCA/maintainer-tools/tree/master/template/module" class="" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">module</span></a></span><span class="separator">/</span><strong class="final-path">README.rst</strong>
  </div>
</div>


  <div class="commit file-history-tease">
    <div class="file-history-tease-header">
        <img alt="@Yajo" class="avatar" data-user="973709" height="24" src="https://avatars2.githubusercontent.com/u/973709?v=3&amp;s=48" width="24" />
        <span class="author"><a href="/Yajo" rel="contributor">Yajo</a></span>
        <time datetime="2015-04-09T11:54:51Z" is="relative-time">Apr 9, 2015</time>
        <div class="commit-title">
            <a href="/OCA/maintainer-tools/commit/3cc4691b002ff8568975a63d64311d006a0800f3" class="message" data-pjax="true" title="Fix typo and sexism.">Fix typo and sexism.</a>
        </div>
    </div>

    <div class="participation">
      <p class="quickstat">
        <a href="#blob_contributors_box" rel="facebox">
          <strong>4</strong>
           contributors
        </a>
      </p>
          <a class="avatar-link tooltipped tooltipped-s" aria-label="Yajo" href="/OCA/maintainer-tools/commits/master/template/module/README.rst?author=Yajo"><img alt="@Yajo" class="avatar" data-user="973709" height="20" src="https://avatars0.githubusercontent.com/u/973709?v=3&amp;s=40" width="20" /> </a>
    <a class="avatar-link tooltipped tooltipped-s" aria-label="max3903" href="/OCA/maintainer-tools/commits/master/template/module/README.rst?author=max3903"><img alt="@max3903" class="avatar" data-user="939952" height="20" src="https://avatars2.githubusercontent.com/u/939952?v=3&amp;s=40" width="20" /> </a>
    <a class="avatar-link tooltipped tooltipped-s" aria-label="pedrobaeza" href="/OCA/maintainer-tools/commits/master/template/module/README.rst?author=pedrobaeza"><img alt="@pedrobaeza" class="avatar" data-user="7165771" height="20" src="https://avatars1.githubusercontent.com/u/7165771?v=3&amp;s=40" width="20" /> </a>
    <a class="avatar-link tooltipped tooltipped-s" aria-label="lmignon" href="/OCA/maintainer-tools/commits/master/template/module/README.rst?author=lmignon"><img alt="@lmignon" class="avatar" data-user="544090" height="20" src="https://avatars3.githubusercontent.com/u/544090?v=3&amp;s=40" width="20" /> </a>


    </div>
    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list">
          <li class="facebox-user-list-item">
            <img alt="@Yajo" data-user="973709" height="24" src="https://avatars2.githubusercontent.com/u/973709?v=3&amp;s=48" width="24" />
            <a href="/Yajo">Yajo</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="@max3903" data-user="939952" height="24" src="https://avatars0.githubusercontent.com/u/939952?v=3&amp;s=48" width="24" />
            <a href="/max3903">max3903</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="@pedrobaeza" data-user="7165771" height="24" src="https://avatars3.githubusercontent.com/u/7165771?v=3&amp;s=48" width="24" />
            <a href="/pedrobaeza">pedrobaeza</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="@lmignon" data-user="544090" height="24" src="https://avatars1.githubusercontent.com/u/544090?v=3&amp;s=48" width="24" />
            <a href="/lmignon">lmignon</a>
          </li>
      </ul>
    </div>
  </div>

<div class="file">
  <div class="file-header">
    <div class="file-actions">

      <div class="btn-group">
        <a href="/OCA/maintainer-tools/raw/master/template/module/README.rst" class="btn btn-sm " id="raw-url">Raw</a>
          <a href="/OCA/maintainer-tools/blame/master/template/module/README.rst" class="btn btn-sm js-update-url-with-hash">Blame</a>
        <a href="/OCA/maintainer-tools/commits/master/template/module/README.rst" class="btn btn-sm " rel="nofollow">History</a>
      </div>


            <form accept-charset="UTF-8" action="/OCA/maintainer-tools/edit/master/template/module/README.rst" class="inline-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="4MDS4qiCF/5uiEB3WmlblcVo9tZqW8j5iJfULDkSI7AS5BOhZwLSETMdYowRYLT6r8kzHZiaKQ+mkqYMocLhXg==" /></div>
              <button class="octicon-btn tooltipped tooltipped-n" type="submit" aria-label="Fork this project and edit the file" data-hotkey="e" data-disable-with>
                <span class="octicon octicon-pencil"></span>
              </button>
</form>
          <form accept-charset="UTF-8" action="/OCA/maintainer-tools/delete/master/template/module/README.rst" class="inline-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="SdQfRaq27bXy0Vmc1gPPgkqCKn2myx/epPmzbQ8hzHeQqh6VCPHYt8J0w40Vemp6ahNHOTU1m/GTzsdxWSJN3w==" /></div>
            <button class="octicon-btn octicon-btn-danger tooltipped tooltipped-n" type="submit" aria-label="Fork this project and delete this file" data-disable-with>
              <span class="octicon octicon-trashcan"></span>
            </button>
</form>    </div>

    <div class="file-info">
        63 lines (39 sloc)
        <span class="file-info-divider"></span>
      1.133 kb
    </div>
  </div>
    <div id="readme" class="blob instapaper_body">
    <article class="markdown-body entry-content" itemprop="mainContentOfPage"><a href="https://camo.githubusercontent.com/88d42f6cede496fc36ca1d6f65746211d8ca40fd/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e63652d4147504c2d2d332d626c75652e737667" target="_blank"><img alt="License: AGPL-3" src="https://camo.githubusercontent.com/88d42f6cede496fc36ca1d6f65746211d8ca40fd/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e63652d4147504c2d2d332d626c75652e737667" data-canonical-src="https://img.shields.io/badge/licence-AGPL--3-blue.svg" style="max-width:100%;"></a>
<a name="user-content-module-name"></a>
<h2>
<a id="user-content-module-name" class="anchor" href="#module-name" aria-hidden="true"><span class="octicon octicon-link"></span></a> Product Variant Inactive </h2>
<p>This module was written to extend the functionality of Product Variants 
and allow you to make activate or deactivate products using the two buttons <img src="img/img.png"> </p>
<a name="user-content-installation"></a>
<h2>
<a id="user-content-installation" class="anchor" href="#installation" aria-hidden="true"><span class="octicon octicon-link"></span></a>Installation</h2>
<p>To install this module, you need to:</p>
<ul>
<li>To install Product </li>
</ul>
<p>For further information, please visit:</p>
<ul>
<li><a href="https://www.odoo.com/forum/help-1">https://www.odoo.com/forum/help-1</a></li>
</ul>
<a name="user-content-contributors"></a>
<h3>
<a id="user-content-contributors" class="anchor" href="#contributors" aria-hidden="true"><span class="octicon octicon-link"></span></a>Contributors</h3>
<ul>
<li>Firstname Lastname &lt;<a href="mailto:sebastien.beau%40akretion.com>sebastien.beau@akretion.com</a>&gt;</li>
<li>Second Person &lt;<a href="mailto:abdessamad.hilali%40akretion.com">abdessamad.hilali@akretion.com</a>&gt;</li>
</ul>
<a name="user-content-maintainer"></a>
<h3>
<a id="user-content-maintainer" class="anchor" href="#maintainer" aria-hidden="true"><span class="octicon octicon-link"></span></a>Maintainer</h3>
<a href="http://odoo-community.org"><img alt="Odoo Community Association" src="https://camo.githubusercontent.com/47828635b5c9032c08c4c6c3db92dcc8299c5fa3/687474703a2f2f6f646f6f2d636f6d6d756e6974792e6f72672f6c6f676f2e706e67" data-canonical-src="http://odoo-community.org/logo.png" style="max-width:100%;"></a>
<p>This module is maintained by the OCA.</p>
<p>OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.</p>
<p>To contribute to this module, please visit <a href="http://odoo-community.org">http://odoo-community.org</a>.</p>

</article>
  </div>

</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" action="" class="js-jump-to-line-form" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="btn">Go</button>
</form></div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer" role="contentinfo">
    <ul class="site-footer-links right">
        <li><a href="https://status.github.com/" data-ga-click="Footer, go to status, text:status">Status</a></li>
      <li><a href="https://developer.github.com" data-ga-click="Footer, go to api, text:api">API</a></li>
      <li><a href="https://training.github.com" data-ga-click="Footer, go to training, text:training">Training</a></li>
      <li><a href="https://shop.github.com" data-ga-click="Footer, go to shop, text:shop">Shop</a></li>
        <li><a href="https://github.com/blog" data-ga-click="Footer, go to blog, text:blog">Blog</a></li>
        <li><a href="https://github.com/about" data-ga-click="Footer, go to about, text:about">About</a></li>

    </ul>

    <a href="https://github.com" aria-label="Homepage">
      <span class="mega-octicon octicon-mark-github" title="GitHub"></span>
</a>
    <ul class="site-footer-links">
      <li>&copy; 2015 <span title="0.05254s from github-fe141-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="https://github.com/site/terms" data-ga-click="Footer, go to terms, text:terms">Terms</a></li>
        <li><a href="https://github.com/site/privacy" data-ga-click="Footer, go to privacy, text:privacy">Privacy</a></li>
        <li><a href="https://github.com/security" data-ga-click="Footer, go to security, text:security">Security</a></li>
        <li><a href="https://github.com/contact" data-ga-click="Footer, go to contact, text:contact">Contact</a></li>
    </ul>
  </div>
</div>


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-suggester-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="fullscreen-contents js-fullscreen-contents" placeholder=""></textarea>
      <div class="suggester-container">
        <div class="suggester fullscreen-suggester js-suggester js-navigation-container"></div>
      </div>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped tooltipped-w" aria-label="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped tooltipped-w"
      aria-label="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>
    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-x flash-close js-ajax-error-dismiss" aria-label="Dismiss error"></a>
      Something went wrong with that request. Please try again.
    </div>
      <script crossorigin="anonymous" src="https://assets-cdn.github.com/assets/frameworks-06533d99d3f0ca9115a0563dec4017e1bfad7758231e12b95a178cef2cdc3d4c.js"></script>
      <script async="async" crossorigin="anonymous" src="https://assets-cdn.github.com/assets/github-59cbed91abaeebed35de0a12f8c3adfea46b14dd56c5019b18a7dcdaf3c88a92.js"></script>
      
      

  </body>
</html>

