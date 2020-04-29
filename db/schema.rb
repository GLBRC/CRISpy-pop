# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `rails
# db:schema:load`. When creating a new database, `rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 2019_12_02_153217) do

  create_table "genes", force: :cascade do |t|
    t.string "name"
    t.text "description"
    t.string "genome"
    t.integer "start_pos"
    t.integer "end_pos"
    t.string "chrom"
    t.integer "has_intron"
    t.integer "has_5_utr"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "offsite_hits", force: :cascade do |t|
    t.string "sgrna_sequence"
    t.integer "offsite_search_id"
    t.string "chrom"
    t.integer "pos"
    t.string "strand"
    t.integer "mismatches"
    t.string "name"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "offsite_searches", force: :cascade do |t|
    t.string "sgrna_sequence"
    t.string "genome"
    t.string "pam_sequence"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "results", force: :cascade do |t|
    t.integer "gene_id"
    t.string "sgrna_sequence"
    t.decimal "perc_activity"
    t.string "chrom"
    t.integer "pos"
    t.string "mismatch_seq"
    t.string "strand"
    t.integer "num_mis_matches"
    t.integer "num_off_site_match"
    t.integer "submission_id"
    t.string "gc"
    t.text "strain_coverage"
    t.string "state"
    t.string "name"
    t.integer "pos_in_gene"
    t.text "comments"
    t.integer "strains_covered"
    t.integer "has_human_hit"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "sessions", force: :cascade do |t|
    t.string "session_id", null: false
    t.text "data"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["session_id"], name: "index_sessions_on_session_id", unique: true
    t.index ["updated_at"], name: "index_sessions_on_updated_at"
  end

  create_table "strains", force: :cascade do |t|
    t.string "name"
    t.text "description"
    t.string "vcf_file"
    t.string "strain_set"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "submissions", force: :cascade do |t|
    t.string "submission_type"
    t.integer "gene_id"
    t.string "pam_sequence"
    t.integer "spacer_length"
    t.integer "strain_id"
    t.string "target_type"
    t.string "created_by"
    t.integer "search_human_genome"
    t.text "sequence"
    t.string "genome"
    t.string "target_name"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "targets", force: :cascade do |t|
    t.string "name"
    t.text "comments"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "users", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.integer "sign_in_count", default: 0, null: false
    t.datetime "current_sign_in_at"
    t.datetime "last_sign_in_at"
    t.string "current_sign_in_ip"
    t.string "last_sign_in_ip"
    t.string "username"
    t.string "display_name"
    t.string "provider"
    t.string "uid"
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["email"], name: "index_users_on_email", unique: true
  end

end
