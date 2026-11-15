# ai_welllog.py
"""
AI-Powered Well Log Analysis Module
Simple rule-based AI for curve recognition and quality checking
"""

import re
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import warnings
from dataclasses import dataclass

@dataclass
class QualityReport:
    """Data class for quality check results"""
    overall_score: float
    issues: List[str]
    warnings: List[str]
    recommendations: List[str]
    curve_quality: Dict[str, float]

# ==============================
# AI CURVE RECOGNITION ENGINE
# ==============================

class AICurveRecognizer:
    """AI-powered curve name recognition using pattern matching"""
    
    def __init__(self):
        # Comprehensive knowledge base of curve patterns
        self.curve_database = {
            'Gamma Ray': {
                'primary_patterns': ['gr', 'gamma', 'gapi'],
                'secondary_patterns': ['natural gamma', 'sgr', 'cgr', 'grac'],
                'units': ['gapi', 'api', 'cps', 'counts'],
                'typical_range': (0, 200),
                'color': '#FF6B35'
            },
            'Density': {
                'primary_patterns': ['rhob', 'den', 'density'],
                'secondary_patterns': ['bhd', 'fdc', 'cdl', 'rho'],
                'units': ['g/cc', 'g/cm3', 'g.cm-3'],
                'typical_range': (1.5, 3.0),
                'color': '#004E89'
            },
            'Neutron Porosity': {
                'primary_patterns': ['nphi', 'neut', 'neutron'],
                'secondary_patterns': ['cnl', 'tnph', 'phi', 'porosity'],
                'units': ['v/v', 'pu', 'dec', '%', 'p.u.'],
                'typical_range': (0, 0.6),
                'color': '#1A936F'
            },
            'Resistivity': {
                'primary_patterns': ['res', 'rt', 'resistivity'],
                'secondary_patterns': ['ild', 'll', 'msfl', 'hrd', 'hrl', 're'],
                'units': ['ohm.m', 'ohm-m', 'ohmm', 'ohm'],
                'typical_range': (0.1, 1000),
                'color': '#6A0572'
            },
            'Depth': {
                'primary_patterns': ['dept', 'depth', 'md'],
                'secondary_patterns': ['measured', 'tvd', 'tvdss'],
                'units': ['m', 'ft', 'meters', 'feet'],
                'typical_range': None,
                'color': '#333333'
            },
            'Caliper': {
                'primary_patterns': ['cal', 'cali', 'caliper'],
                'secondary_patterns': ['hole', 'bit', 'diameter'],
                'units': ['in', 'inch', 'cm'],
                'typical_range': (6, 20),
                'color': '#FF9E00'
            },
            'Sonic': {
                'primary_patterns': ['dt', 'sonic'],
                'secondary_patterns': ['ac', 'delta t', 'travel time'],
                'units': ['us/ft', 'us/m', 'μs/ft'],
                'typical_range': (40, 140),
                'color': '#118AB2'
            },
            'Spontaneous Potential': {
                'primary_patterns': ['sp', 'spont'],
                'secondary_patterns': ['potential', 'sp_log'],
                'units': ['mv', 'millivolt'],
                'typical_range': (-200, 200),
                'color': '#8D99AE'
            }
        }
        
        # Common abbreviations mapping
        self.abbreviation_map = {
            'gr': 'Gamma Ray',
            'gapi': 'Gamma Ray',
            'rhob': 'Density',
            'den': 'Density',
            'nphi': 'Neutron Porosity',
            'phi': 'Neutron Porosity',
            'res': 'Resistivity',
            'rt': 'Resistivity',
            'dept': 'Depth',
            'md': 'Depth',
            'cal': 'Caliper',
            'dt': 'Sonic',
            'sp': 'Spontaneous Potential'
        }
    
    def preprocess_curve_name(self, name: str) -> str:
        """Clean and normalize curve names for pattern matching"""
        if not isinstance(name, str):
            name = str(name)
        
        # Convert to lowercase
        name = name.lower()
        
        # Remove special characters but keep spaces and dots
        name = re.sub(r'[^\w\s\.]', ' ', name)
        
        # Replace underscores, dashes, and dots with spaces
        name = name.replace('_', ' ').replace('-', ' ').replace('.', ' ')
        
        # Remove extra spaces
        name = re.sub(r'\s+', ' ', name).strip()
        
        return name
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two strings (0-1 scale)"""
        # Simple similarity calculation
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def extract_units(self, curve_name: str) -> Optional[str]:
        """Extract measurement units from curve name"""
        unit_patterns = {
            'gapi': 'GAPI',
            'api': 'API',
            'g/cc': 'g/cc',
            'g.cm-3': 'g/cc',
            'g/cm3': 'g/cc',
            'ohm.m': 'ohm.m',
            'ohm-m': 'ohm.m',
            'ohmm': 'ohm.m',
            'v/v': 'v/v',
            'pu': 'p.u.',
            '%': '%',
            'us/ft': 'μs/ft',
            'us/m': 'μs/m',
            'μs/ft': 'μs/ft',
            'in': 'in',
            'inch': 'in',
            'ft': 'ft',
            'm': 'm',
            'meters': 'm',
            'feet': 'ft',
            'mv': 'mV'
        }
        
        for pattern, unit in unit_patterns.items():
            if pattern in curve_name.lower():
                return unit
        
        return None
    
    def recognize_single_curve(self, curve_name: str) -> Dict:
        """Recognize a single curve name with confidence score"""
        original_name = curve_name
        clean_name = self.preprocess_curve_name(curve_name)
        units = self.extract_units(curve_name)
        
        # Step 1: Check abbreviation map (fastest)
        if clean_name in self.abbreviation_map:
            return {
                'original': original_name,
                'recognized': self.abbreviation_map[clean_name],
                'confidence': 1.0,
                'units': units,
                'method': 'abbreviation'
            }
        
        # Step 2: Pattern matching
        best_match = None
        best_score = 0
        best_method = ""
        
        for curve_type, info in self.curve_database.items():
            # Check primary patterns
            for pattern in info['primary_patterns']:
                if pattern in clean_name:
                    score = 0.9  # High confidence for primary pattern
                    if score > best_score:
                        best_score = score
                        best_match = curve_type
                        best_method = 'primary_pattern'
            
            # Check secondary patterns
            for pattern in info['secondary_patterns']:
                similarity = self.calculate_similarity(clean_name, pattern)
                if similarity > 0.5:  # Reasonable match
                    score = similarity * 0.8  # Slightly lower confidence
                    if score > best_score:
                        best_score = score
                        best_match = curve_type
                        best_method = 'secondary_pattern'
            
            # Check unit compatibility
            if units and 'units' in info:
                if any(unit in units.lower() for unit in info['units']):
                    # Boost score if units match
                    best_score = min(best_score + 0.1, 1.0)
        
        # Step 3: If no good match found
        if best_score < 0.5:
            # Try to guess based on partial matches
            for curve_type, info in self.curve_database.items():
                for pattern in info['primary_patterns'] + info['secondary_patterns']:
                    if len(pattern) > 3 and pattern in clean_name:
                        return {
                            'original': original_name,
                            'recognized': curve_type,
                            'confidence': 0.6,
                            'units': units,
                            'method': 'partial_match'
                        }
        
        return {
            'original': original_name,
            'recognized': best_match or 'Unknown',
            'confidence': best_score,
            'units': units,
            'method': best_method or 'low_confidence'
        }
    
    def recognize_all_curves(self, curve_names: List[str]) -> Dict:
        """Recognize multiple curves at once"""
        results = {}
        for curve_name in curve_names:
            results[curve_name] = self.recognize_single_curve(curve_name)
        return results
    
    def create_rename_mapping(self, curve_names: List[str], 
                            min_confidence: float = 0.6) -> Dict[str, str]:
        """Create a rename mapping for DataFrame columns"""
        rename_map = {}
        recognition_results = {}
        
        for curve_name in curve_names:
            result = self.recognize_single_curve(curve_name)
            recognition_results[curve_name] = result
            
            if result['confidence'] >= min_confidence:
                rename_map[curve_name] = result['recognized']
            else:
                # Keep original name if low confidence
                rename_map[curve_name] = curve_name
        
        return rename_map, recognition_results

# ==============================
# AI QUALITY CHECK ENGINE
# ==============================

class AIQualityChecker:
    """AI-powered quality checking for well log data"""
    
    def __init__(self):
        # Quality thresholds
        self.thresholds = {
            'missing_data_critical': 0.4,    # >40% missing = critical
            'missing_data_warning': 0.2,     # >20% missing = warning
            'spike_threshold': 3.0,          # 3 std deviations for spikes
            'depth_reversal_limit': 5,       # Max allowed depth reversals
            'range_violation_threshold': 0.1, # 10% outside typical range
            'constant_value_limit': 0.95     # 95% same value = stuck tool
        }
        
        # Typical value ranges for common curves
        self.typical_ranges = {
            'Gamma Ray': (0, 200),
            'Density': (1.5, 3.0),
            'Neutron Porosity': (0, 0.6),
            'Resistivity': (0.1, 1000),
            'Caliper': (6, 20),
            'Sonic': (40, 140),
            'Spontaneous Potential': (-200, 200)
        }
    
    def check_depth_quality(self, depth_data: pd.Series) -> Tuple[List[str], float]:
        """Check depth-related issues"""
        issues = []
        depth_score = 1.0
        
        if depth_data is None or len(depth_data) == 0:
            return ["No depth data available"], 0.0
        
        # Convert to Series if it's an index
        if isinstance(depth_data, pd.Index):
            depth_data = pd.Series(depth_data)
        
        # Check 1: Depth monotonicity
        depth_diffs = depth_data.diff().dropna()
        
        # Count reversals (negative differences)
        reversals = (depth_diffs < 0).sum()
        if reversals > self.thresholds['depth_reversal_limit']:
            issues.append(f"⚠️ Depth reversals detected: {reversals} points")
            depth_score -= 0.3
        
        # Check 2: Large gaps
        if len(depth_diffs) > 1:
            median_diff = depth_diffs.median()
            if median_diff > 0:  # Avoid division by zero
                large_gaps = (depth_diffs > 2 * median_diff).sum()
                if large_gaps > 0:
                    issues.append(f"⚠️ Large depth gaps detected: {large_gaps} intervals")
                    depth_score -= 0.2
        
        # Check 3: Constant depth (stuck tool)
        unique_depths = depth_data.nunique()
        if unique_depths < len(depth_data) * 0.1:
            issues.append("🚨 Possible stuck tool - many repeated depth values")
            depth_score -= 0.5
        
        # Check 4: Regular sampling
        if len(depth_diffs) > 2:
            cv = depth_diffs.std() / depth_diffs.mean()
            if cv > 0.2:
                issues.append("⚠️ Irregular depth sampling detected")
                depth_score -= 0.1
        
        return issues, max(depth_score, 0.0)
    
    def check_missing_data(self, df: pd.DataFrame) -> Tuple[List[str], Dict[str, float]]:
        """Check for missing data issues"""
        issues = []
        curve_scores = {}
        
        for column in df.columns:
            missing_pct = df[column].isna().mean()
            
            # Calculate score for this curve
            curve_score = 1.0 - missing_pct
            curve_scores[column] = max(curve_score, 0.0)
            
            if missing_pct > self.thresholds['missing_data_critical']:
                issues.append(f"🚨 Critical: '{column}' has {missing_pct:.1%} missing data")
                curve_scores[column] *= 0.5
            elif missing_pct > self.thresholds['missing_data_warning']:
                issues.append(f"⚠️ Warning: '{column}' has {missing_pct:.1%} missing data")
                curve_scores[column] *= 0.8
            
            # Check for block missing data
            if missing_pct > 0:
                missing_mask = df[column].isna()
                missing_runs = (missing_mask != missing_mask.shift()).cumsum()
                run_lengths = missing_mask.groupby(missing_runs).sum()
                
                if run_lengths.max() > 20:
                    issues.append(f"⚠️ '{column}' has block missing data (possible tool issues)")
        
        return issues, curve_scores
    
    def check_value_ranges(self, df: pd.DataFrame, 
                          curve_types: Dict) -> Tuple[List[str], Dict[str, float]]:
        """Check if values are within typical ranges"""
        warnings = []
        curve_scores = {}
        
        for column in df.columns:
            curve_score = 1.0
            data = df[column].dropna()
            
            if len(data) == 0:
                continue
            
            # Get curve type from recognition results
            curve_info = curve_types.get(column, {})
            curve_name = curve_info.get('recognized', '')
            
            # Check against typical ranges
            if curve_name in self.typical_ranges:
                min_val, max_val = self.typical_ranges[curve_name]
                
                # Calculate percentage of data outside range
                outside_min = (data < min_val).mean()
                outside_max = (data > max_val).mean()
                total_outside = outside_min + outside_max
                
                if total_outside > 0:
                    # Reduce score based on how much is outside range
                    curve_score -= total_outside * 0.5
                    
                    if total_outside > self.thresholds['range_violation_threshold']:
                        warnings.append(
                            f"⚠️ '{column}' has {total_outside:.1%} values "
                            f"outside typical range ({min_val}-{max_val})"
                        )
            
            # Check for constant values (stuck tool)
            unique_ratio = data.nunique() / len(data)
            if unique_ratio < (1 - self.thresholds['constant_value_limit']):
                warnings.append(f"🚨 '{column}' may have stuck tool (constant values)")
                curve_score *= 0.3
            
            curve_scores[column] = max(curve_score, 0.0)
        
        return warnings, curve_scores
    
    def check_statistical_issues(self, df: pd.DataFrame) -> Tuple[List[str], Dict[str, float]]:
        """Check for statistical anomalies"""
        warnings = []
        curve_scores = {}
        
        for column in df.columns:
            curve_score = 1.0
            data = df[column].dropna()
            
            if len(data) < 10:
                continue
            
            # Check for spikes (sudden large changes)
            if len(data) > 1:
                z_scores = np.abs((data - data.mean()) / data.std())
                spikes = (z_scores > self.thresholds['spike_threshold']).sum()
                
                spike_ratio = spikes / len(data)
                if spike_ratio > 0.05:  # More than 5% spikes
                    warnings.append(f"⚠️ '{column}' has {spikes} statistical spikes")
                    curve_score -= spike_ratio * 0.3
            
            # Check for outliers using IQR method
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).sum()
            
            outlier_ratio = outliers / len(data)
            if outlier_ratio > 0.1:  # More than 10% outliers
                warnings.append(f"⚠️ '{column}' has {outliers} potential outliers")
                curve_score -= outlier_ratio * 0.2
            
            curve_scores[column] = max(curve_score, 0.0)
        
        return warnings, curve_scores
    
    def check_curve_consistency(self, df: pd.DataFrame, 
                               curve_types: Dict) -> List[str]:
        """Check if curves make sense together"""
        suggestions = []
        
        # Check density-neutron relationship
        density_col = None
        neutron_col = None
        
        for col, info in curve_types.items():
            if info.get('recognized') == 'Density':
                density_col = col
            elif info.get('recognized') == 'Neutron Porosity':
                neutron_col = col
        
        if density_col and neutron_col and density_col in df.columns and neutron_col in df.columns:
            density = df[density_col].dropna()
            neutron = df[neutron_col].dropna()
            
            if len(density) > 10 and len(neutron) > 10:
                # Simple crossover check
                crossover = (density.mean() < 2.3) and (neutron.mean() > 0.2)
                if crossover:
                    suggestions.append("📊 Density-Neutron crossover detected - possible gas zone")
        
        return suggestions
    
    def comprehensive_quality_check(self, df: pd.DataFrame, 
                                  curve_recognition: Dict) -> QualityReport:
        """Run all quality checks and generate comprehensive report"""
        all_issues = []
        all_warnings = []
        recommendations = []
        curve_quality_scores = {}
        
        # Initialize all curve scores to 1.0
        for col in df.columns:
            curve_quality_scores[col] = 1.0
        
        # 1. Depth quality check
        if df.index.name == 'Depth' or 'Depth' in df.columns:
            depth_data = df.index if df.index.name == 'Depth' else df['Depth']
            depth_issues, depth_score = self.check_depth_quality(depth_data)
            all_issues.extend(depth_issues)
            
            # Update curve score for depth
            if 'Depth' in df.columns:
                curve_quality_scores['Depth'] = depth_score
        
        # 2. Missing data check
        missing_issues, missing_scores = self.check_missing_data(df)
        all_issues.extend(missing_issues)
        
        # Update curve scores with missing data factor
        for col, score in missing_scores.items():
            curve_quality_scores[col] *= score
        
        # 3. Value range check
        range_warnings, range_scores = self.check_value_ranges(df, curve_recognition)
        all_warnings.extend(range_warnings)
        
        # Update curve scores with range factor
        for col, score in range_scores.items():
            curve_quality_scores[col] *= score
        
        # 4. Statistical issues check
        stat_warnings, stat_scores = self.check_statistical_issues(df)
        all_warnings.extend(stat_warnings)
        
        # Update curve scores with statistical factor
        for col, score in stat_scores.items():
            curve_quality_scores[col] *= score
        
        # 5. Curve consistency check
        consistency_suggestions = self.check_curve_consistency(df, curve_recognition)
        recommendations.extend(consistency_suggestions)
        
        # Generate overall recommendations
        if all_issues:
            recommendations.append("🔧 Consider data reprocessing or filtering")
        
        if len(all_warnings) > 5:
            recommendations.append("📈 Perform detailed quality control analysis")
        
        if 'Gamma Ray' in str(df.columns) and 'Resistivity' in str(df.columns):
            recommendations.append("💡 Run basic quick-look interpretation for reservoir identification")
        
        # Calculate overall quality score
        if curve_quality_scores:
            overall_score = np.mean(list(curve_quality_scores.values()))
        else:
            overall_score = 0.0
        
        # Adjust score based on number of critical issues
        critical_issues = len([i for i in all_issues if '🚨' in i])
        overall_score -= critical_issues * 0.1
        
        # Ensure score is between 0 and 1
        overall_score = max(0.0, min(1.0, overall_score))
        
        return QualityReport(
            overall_score=overall_score,
            issues=all_issues,
            warnings=all_warnings,
            recommendations=recommendations,
            curve_quality=curve_quality_scores
        )

# ==============================
# MAIN PROCESSING FUNCTION
# ==============================

def process_well_log_with_ai(file_path: str, min_confidence: float = 0.6):
    """
    Complete AI processing pipeline for well log data
    
    Parameters:
    -----------
    file_path : str
        Path to LAS file
    min_confidence : float
        Minimum confidence for curve recognition (0-1)
    
    Returns:
    --------
    Dict containing all processing results
    """
    import lasio
    
    # Read LAS file
    las = lasio.read(file_path)
    df = las.df()
    original_columns = df.columns.tolist()
    
    # Initialize AI modules
    recognizer = AICurveRecognizer()
    checker = AIQualityChecker()
    
    # 1. AI Curve Recognition
    rename_map, recognition_results = recognizer.create_rename_mapping(
        original_columns, min_confidence
    )
    
    # 2. Apply renaming
    df_renamed = df.rename(columns=rename_map)
    
    # 3. AI Quality Check
    quality_report = checker.comprehensive_quality_check(df_renamed, recognition_results)
    
    # 4. Prepare results
    results = {
        'original_df': df,
        'renamed_df': df_renamed,
        'original_columns': original_columns,
        'rename_map': rename_map,
        'recognition_results': recognition_results,
        'quality_report': quality_report,
        'well_info': {
            'file_path': file_path,
            'depth_range': (df.index.min(), df.index.max()) if len(df) > 0 else (0, 0),
            'curve_count': len(df.columns),
            'data_points': len(df),
            'has_depth': 'Depth' in rename_map.values()
        }
    }
    
    return results

def get_quality_color(score: float) -> str:
    """Get color based on quality score"""
    if score >= 0.8:
        return "#4CAF50"  # Green
    elif score >= 0.6:
        return "#FFC107"  # Yellow/Amber
    elif score >= 0.4:
        return "#FF9800"  # Orange
    else:
        return "#F44336"  # Red

def get_quality_emoji(score: float) -> str:
    """Get emoji based on quality score"""
    if score >= 0.8:
        return "🟢"  # Green circle
    elif score >= 0.6:
        return "🟡"  # Yellow circle
    elif score >= 0.4:
        return "🟠"  # Orange circle
    else:
        return "🔴"  # Red circle

def summarize_quality_report(report: QualityReport) -> str:
    """Create a human-readable summary of quality report"""
    summary = []
    
    # Overall score
    emoji = get_quality_emoji(report.overall_score)
    summary.append(f"{emoji} Overall Quality: {report.overall_score:.0%}")
    
    # Issues
    if report.issues:
        summary.append(f"\n🚨 Critical Issues ({len(report.issues)}):")
        for issue in report.issues[:3]:  # Show only first 3
            summary.append(f"  • {issue}")
        if len(report.issues) > 3:
            summary.append(f"  ... and {len(report.issues) - 3} more")
    
    # Warnings
    if report.warnings:
        summary.append(f"\n⚠️ Warnings ({len(report.warnings)}):")
        for warning in report.warnings[:3]:  # Show only first 3
            summary.append(f"  • {warning}")
        if len(report.warnings) > 3:
            summary.append(f"  ... and {len(report.warnings) - 3} more")
    
    # Recommendations
    if report.recommendations:
        summary.append(f"\n💡 Recommendations:")
        for rec in report.recommendations:
            summary.append(f"  • {rec}")
    
    return "\n".join(summary)

# Test function
def test_ai_module():
    """Test the AI module functionality"""
    print("=" * 60)
    print("AI Well Log Module - Test")
    print("=" * 60)
    
    # Test curve recognition
    recognizer = AICurveRecognizer()
    test_names = ["GR", "RHOB_COR", "NPHI_DOL", "RT", "DEPTH", "UNKNOWN"]
    
    print("\n🔍 Testing Curve Recognition:")
    for name in test_names:
        result = recognizer.recognize_single_curve(name)
        print(f"  {name:15} → {result['recognized']:20} "
              f"(Confidence: {result['confidence']:.2f})")
    
    # Test quality checker with sample data
    print("\n📊 Testing Quality Checker:")
    np.random.seed(42)
    n_points = 100
    
    # Create sample DataFrame
    df = pd.DataFrame({
        'Depth': np.linspace(1000, 1100, n_points),
        'Gamma Ray': np.random.uniform(50, 150, n_points),
        'Density': np.random.normal(2.3, 0.2, n_points),
        'Neutron Porosity': np.random.uniform(0.15, 0.35, n_points)
    })
    
    # Add some issues
    df.loc[10:20, 'Density'] = np.nan  # Missing data
    df.loc[5, 'Gamma Ray'] = 500  # Outlier
    
    checker = AIQualityChecker()
    curve_types = {
        'Depth': {'recognized': 'Depth'},
        'Gamma Ray': {'recognized': 'Gamma Ray'},
        'Density': {'recognized': 'Density'},
        'Neutron Porosity': {'recognized': 'Neutron Porosity'}
    }
    
    report = checker.comprehensive_quality_check(df, curve_types)
    
    print(f"\n📈 Quality Score: {report.overall_score:.0%}")
    print(f"📋 Issues found: {len(report.issues)}")
    print(f"⚠️  Warnings: {len(report.warnings)}")
    
    print("\n" + "=" * 60)
    print("✅ AI Module Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_ai_module()