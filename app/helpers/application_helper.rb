module ApplicationHelper
  def pagination_widget(collection, opts = {})
    collection.load unless collection.loaded?
    entry_name = opts.delete(:entry_name)

    content_tag :div, class: 'pagination-widget' do
      concat(content_tag(:div, class: 'page-links') do
        paginate(collection, opts)
      end)
      concat(content_tag(:div, class: 'page-info') do
        page_entries_info(collection, entry_name: entry_name)
      end)
    end
  end

  def fa_text(css, text)
    "<i class='fa #{css} fa-fw'></i> #{text}".html_safe
  end

  def card(title, bootstrap_width, options = {}, &block)
    block_to_partial('shared/card', options.merge(title: title, bootstrap_width: bootstrap_width), &block)
  end

  def nav_tabs(tab_names, active_tab_id, options = {}, &block)
    options[:class_list] ||= ''
    options[:tab_ids] ||= {}
    tab_names.each do |tab_name|
      options[:tab_ids][tab_name.to_sym] ||= "#{tab_name.parameterize}-tab"
    end
    block_to_partial('shared/nav_tabs', options.merge(tab_names: tab_names, active_tab_id: active_tab_id), &block)
  end

  # Use in conjunction with ApplicationHelper#nav_tabs.
  def tab(tab_name, active_tab_id, options = {}, &block)
    options[:id] ||= "#{tab_name.parameterize}-tab"
    block_to_partial('shared/tab', options.merge(tab_name: tab_name, active_tab_id: active_tab_id), &block)
  end

  def sortable(column, title = nil, _params_hash = nil)
    title ||= column.titleize
    icon = ''
    if column == sort_column
      if sort_direction == 'asc'
        icon = " <i class='fa fa-caret-up'/>"
      else
        icon = " <i class='fa fa-caret-down'/>"
      end
    end

    search = params[:search]
    direction = column == sort_column && sort_direction == 'asc' ? 'desc' : 'asc'
    link_to (title + icon).html_safe, { search: search, sort: column, direction: direction }, style: 'color: white;white-space: nowrap'
  end

  def block_to_partial(partial_name, options = {}, &block)
    # capture block output into 'body' and merge it into our options hash
    options[:body] = capture(&block)
    # render partial with options hash, per usual
    concat(render(partial: partial_name, locals: options))
  end

  # copied out of application helper in Data Catalog
  def filter_link(parent_type, opts = { active: nil })
    is_active = ''
    if params[:filters] && params[:filters][:parent_type]
      is_active = parent_type == params[:filters][:parent_type] ? 'active' : ''
    end
    link_to parent_type.titleize, params.permit(:active, :filters).merge(
      active: opts[:active],
      filters: { parent_type: parent_type }
    ), class: "btn btn-outline-secondary #{is_active}", id: "filter-#{parent_type}"
  end
end
